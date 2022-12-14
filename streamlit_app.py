import os
from typing import Optional

import streamlit as st

from app import parse, secrets, static, badges
from common import Reader, get_module

PAGE_ICON_PATH = "images/aoc-icon.png"
SIDEBAR_IMAGE_PATH = "images/aoc-balloon-grey.png"


def render_page(last_day: int, selected_day: int = None):
    session_id = secrets.get_session_id()
    days_info = _get_info(last_day, session_id)

    selected_day_number = _select_from_sidebar(days=[d.title for d in days_info], selected=selected_day)
    day_info = days_info[selected_day_number]

    st.subheader(f'[{day_info.title[4:-4]}]({day_info.url})' if day_info.title != parse.PARSE_EMPTY else '')
    col_task, col_solution = st.columns(2, gap='large')
    with col_task:
        _print_task(day_info.texts)
    with col_solution:
        _print_input(selected_day_number+1)
        _print_solution(selected_day_number+1)


@st.cache(ttl=3600, allow_output_mutation=True)
def _get_info(last_day: int, session_id: str):
    return parse.get_day_info(last_day, session_id)


@st.cache(ttl=3600)
def _get_input(_day: int):
    reader = Reader(day=_day, is_test=False)
    return reader.get_data() if reader.path_exists() else ""


def _get_day_from_query(par: dict) -> Optional[int]:
    if 'day' not in par:
        return None

    day_str = par['day'][0]
    day_int = int(day_str) if day_str.isdigit() else None
    return day_int


def _select_from_sidebar(days: list, selected: int):
    with st.sidebar:
        _, col_img, _ = st.columns((1, 4, 1))
        col_img.image(SIDEBAR_IMAGE_PATH)
        selected_day_number = st.radio(
            label='Select a day',
            options=range(len(days)),
            index=0 if (not selected) or (selected < 1) or (selected > 25) else selected-1,
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
    data = _get_input(selected_day)
    st.markdown('#### My Input')
    if not data:
        st.warning('No input file')
        return

    show = st.checkbox(
        label='Show input',
        value=False,
        help=static.input_caution
    )
    if not show:
        return

    with st.expander('Expand'):
        st.code(data)


def _print_solution(selected_day: int):
    st.markdown('#### Solution')
    solution_path = f'./solutions/day{selected_day:02}.py'
    if not os.path.exists(solution_path):
        st.warning('No solution provided yet')
        return

    with open(solution_path) as f:
        source = f.read()

    st.code(source)


def add_badges_to_sidebar(*bs):
    all_badges: dict = badges.badges
    for i in range(0, len(bs), 2):
        line = all_badges[bs[i]].url + all_badges[bs[i + 1]].url
        st.sidebar.markdown(line)


st.set_page_config(page_icon=PAGE_ICON_PATH, page_title='Aoc22 Solutions', layout='wide')
st.title(static.header)
st.info(static.annotation)
st.caption(static.disclaimer)
st.markdown('----')

params = st.experimental_get_query_params()
day = _get_day_from_query(params)

render_page(last_day=25, selected_day=day)
add_badges_to_sidebar('linkedin', 'github')
