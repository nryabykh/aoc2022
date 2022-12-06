import streamlit as st
import inspect

from app import parse
from common import get_module, Reader


def run(last_day: int):
    days_info = _get_info(last_day)

    selected_day_number = _select_from_sidebar(days=[d.title for d in days_info])
    day_info = days_info[selected_day_number]

    st.subheader(f'[{day_info.title[4:-4]}]({day_info.url})' if day_info.title != parse.PARSE_EMPTY else '')
    st.markdown('----')
    col_task, col_solution = st.columns(2, gap='large')
    with col_task:
        _print_task(day_info.texts)
    with col_solution:
        _print_input(selected_day_number+1)
        _print_solution(selected_day_number+1)


@st.cache(ttl=3600)
def _get_info(last_day: int):
    return parse.get_day_info(last_day)


@st.cache(ttl=3600)
def _get_input(day: int):
    reader = Reader(day=day, is_test=False)
    return reader.get_data() if reader.path_exists() else ""


def _select_from_sidebar(days: list):
    with st.sidebar:
        st.image('images/aoc-balloon.png')
        selected_day_number = st.radio(
            label='Select a day',
            options=range(len(days)),
            format_func=lambda x: days[x][4:-4] if days[x] != parse.PARSE_EMPTY else days[x]
        )
    return selected_day_number


def _print_task(texts: list):
    st.markdown('#### Puzzle')
    if not texts:
        st.warning('No task available yet')

    part = ""
    for tag, text in texts:
        if tag == 'p':
            if text.startswith('Your puzzle answer'):
                part = 'One' if not part else 'Two'
                text = text.replace('Your puzzle answer was', f'#### Part {part} answer is')
        if tag == 'p':
            st.markdown(text)
        else:
            st.code(text)
        if part == 'Two':
            break


def _print_input(selected_day: int):
    caution_text = """Many lines, a lot of scroll, browser
     slowdown. But you can copy the whole input and reproduce the solution!"""

    data = _get_input(selected_day)
    st.markdown('#### My Input')
    if not data:
        st.warning('No input file')
        return

    show = st.checkbox(
        label='Show input',
        value=False,
        help=caution_text
    )
    if not show:
        return

    with st.expander('Expand'):
        st.code(data)


def _print_solution(selected_day: int):
    st.markdown('#### Solution')
    try:
        cls = get_module(selected_day)
    except ModuleNotFoundError as _:
        st.warning('No solution provided yet')
        return

    comment = """# Input lines stored in self.data['input']\n\n"""
    st.code(comment + inspect.getsource(cls))


st.set_page_config(page_icon='images/aoc-icon.png', page_title='Aoc22 Solutions', layout='wide')
st.title('Advent of Code 2022')
st.caption("""Below you can find inputs and answers eligible for my AoC account only. For you, there are other 
    inputs and other answers obviously. So copying and pasting my answers to your puzzles does not make any sense.""")

run(last_day=7)
