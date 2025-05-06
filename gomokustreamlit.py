import streamlit as st  
import pandas as pd
import string
from gomoku import Gomoku, GomokuBot, GomokuPos, BOARD_SIZE

BOT_MOVE_LETTER = 'X'
HUMAN_MOVE_LETTER = 'O'
row_names = list(range(1, BOARD_SIZE + 1))
column_names = list(string.ascii_uppercase)[:BOARD_SIZE]


row = st.selectbox('Select row', options=row_names)
col = st.selectbox('Select column', options=column_names)

if 'game' not in st.session_state:
    st.session_state.game = Gomoku().serialize()
    data = pd.DataFrame([[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)])
    data.columns = column_names
    data.index = row_names
    st.session_state.data = data
    st.session_state.last_changed_cell = None
    st.session_state.have_not_any_move_yet = True
    st.session_state.current_is_human_move = False
    st.session_state.winner = 'N'


st.markdown("""
    <style>
        table, th, td {
            border: 1px solid black;
            border-collapse: collapse;
            font-size: 20px;
        }
        th, td {
            padding: 5px 10px;
        }
    </style>
""", unsafe_allow_html=True)


def draw_to_UI(number_row, letter_column, moved_letter):
    st.session_state.data.loc[number_row, letter_column] = moved_letter
    st.session_state.last_changed_cell = (number_row, letter_column)


status_bar = st.empty()
def show_status(msg):
    status_bar.markdown(f"**{msg}**", unsafe_allow_html=True)

def bot_make_move():
    show_status("Bot is thinking, please be patient... 🤖")
    game = Gomoku.deserialize(st.session_state.game)
    bot = GomokuBot(game)
    bot_turn = bot.take_turn_alpha_beta()
    bot_number_row, bot_letter_column = bot_turn.to_standard_pos()
    game.move(bot_turn)
    draw_to_UI(bot_number_row, bot_letter_column, BOT_MOVE_LETTER)
    st.session_state.game = game.serialize()
    st.session_state.winner = Gomoku.deserialize(st.session_state.game).win()
    st.session_state.current_is_human_move = True
    show_status("Bot moved!")

def show_winner(winner):
    if winner == 'X':
        st.success('Bot (X) wins!')
    elif winner == 'O':
        st.success('Human (O) wins!')
    else:
        st.info('It\'s a Tie!')


if st.button('Move'):
    if st.session_state.winner == 'N':
        game = Gomoku.deserialize(st.session_state.game)
        gomoku_pos = GomokuPos.to_gomoku_pos(row, col)
        if not game.have_occupied(gomoku_pos):
            draw_to_UI(row, col, HUMAN_MOVE_LETTER)
            game.move(gomoku_pos)
            st.session_state.game = game.serialize()
            st.session_state.winner = Gomoku.deserialize(st.session_state.game).win()
            st.session_state.current_is_human_move = False
            st.rerun()  
        else:
            show_status(f"Sorry, cell {row}{col} is already occupied!")


if st.button('Replay'):
    st.session_state.game = Gomoku().serialize()
    data = pd.DataFrame([[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)])
    data.columns = column_names
    data.index = row_names
    st.session_state.data = data
    st.session_state.last_changed_cell = None
    st.session_state.have_not_any_move_yet = True
    st.session_state.current_is_human_move = False
    st.session_state.winner = 'N'
    show_status("Game reset! Let's play again...")


if st.session_state.winner != 'N':
    show_winner(st.session_state.winner)


html_table = "<table><tr><th></th>"
for col in column_names:
    html_table += f'<th style="text-align: center;">{col}</th>'
html_table += "</tr>"
for i, (index, row_data) in enumerate(st.session_state.data.iterrows(), 1):
    html_table += "<tr>"
    html_table += f'<th style="text-align: center;">{index}</th>'
    for j, cell in enumerate(row_data):
        text_color = "red" if cell == 'O' else "blue" if cell == 'X' else "black"
        highlight = 'background-color: yellow;' if st.session_state.last_changed_cell == (i, column_names[j]) else ''
        html_table += f'<td style="text-align: center; color: {text_color}; {highlight}">{cell}</td>'
    html_table += "</tr>"
html_table += "</table>"
st.write(html_table, unsafe_allow_html=True)


if (not st.session_state.current_is_human_move or st.session_state.have_not_any_move_yet) and st.session_state.winner == 'N':
    st.session_state.have_not_any_move_yet = False
    bot_make_move()
