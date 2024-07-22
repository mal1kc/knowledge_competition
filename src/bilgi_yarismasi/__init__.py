import os
import random
import tkinter
from tkinter import Tk, Toplevel, ttk
from pprint import pprint
from typing import Any  # pyright: ignore[reportAny]

import pytomlpp

QUESTIONS_DATA_FILE = "sorular.toml"

LEARDERBOARD_DATA_FILE = "lider_tablosu.toml"

TK_THEME = os.path.dirname(__file__) + "/sun-valley.tcl"


def get_toml_data(filename: str) -> dict[Any, Any]:
    with open(filename, mode="r", encoding="utf-8") as f:
        data = pytomlpp.load(f)  # pyright: ignore[reportUnknownMemberType]
    return data


def save_toml_data(filename: str, data: dict[str, Any]) -> None:
    with open(filename, mode="w", encoding="utf-8") as f:
        pytomlpp.dump(data, f)  # pyright: ignore[reportUnknownMemberType]


class KnowledgeCompetition:
    def __init__(self, root: Tk) -> None:
        # definitions

        self.username_window: Toplevel
        self.username_input: tkinter.Text
        self.username_input_label: ttk.Label
        self.username_window_button: ttk.Button

        self.leaderboard_window: Toplevel
        self.leaderboard_paned: ttk.PanedWindow
        self.leaderboard_treeview: ttk.Treeview
        self.leaderboard_toggle_btn: ttk.Button
        self.ld_frame: ttk.Frame
        self.ld_scrollbar: ttk.Scrollbar

        self.left_frame: ttk.Frame
        self.middle_frame: ttk.Frame
        self.details_frame: ttk.Frame
        self.question_frame: ttk.Frame
        self.answers_frame: ttk.Frame

        self.quit_button_btn: ttk.Button
        self.adventage1_btn: ttk.Button
        self.adventage2_btn: ttk.Button
        self.adventage3_btn: ttk.Button

        self.answer1_btn: ttk.Button
        self.answer2_btn: ttk.Button
        self.answer3_btn: ttk.Button
        self.answer4_btn: ttk.Button

        self.question_object_text: str
        self.corret_answer: str

        self.answers_texts: list[str]

        self.question_object_label: ttk.Label
        self.user_lives_label: ttk.Label
        self.question_label: ttk.Label

        self.content: ttk.Separator

        self.questions_data: dict[str, list[dict[str, str]]]
        self.current_question_data: dict[str, str]

        self.user_point = 0

        self.user_lives = 3

        self.min_asked = 0

        self.user_rightAnswers = 0
        self.username = str()

        self.special_skills_states = [False, False, False]

        self.temp: dict[str, list[dict[str, str]]] = dict()

        self.temp["question"] = list()
        self.root = root

        _ = self.root.columnconfigure(0, weight=1)

        _ = self.root.rowconfigure(0, weight=1)

        # self.root.config(bg="black")

        self.root.title("bilgi yarışması")

        self.main_frame = ttk.Frame(self.root)

        self.main_frame.grid(row=0, column=0)

        _ = self.main_frame.grid_rowconfigure(0, weight=0)

        _ = self.main_frame.grid_columnconfigure(0, weight=0)

        # Set the initial theme

        self.root.tk.call("source", TK_THEME)

        self.root.tk.call("set_theme", "dark")

        self.left_part()
        self.middle_part()

        # self.right_part()

        # ! debıg

        # self.username = "malik"
        self.get_username()

        self.get_questions_data()

        self.temp = self.questions_data

        self.update_middle()

    def left_part(self):
        self.left_frame = ttk.Frame(self.main_frame, padding=(20, 20))
        self.left_frame.grid(
            column=0, row=0, padx=(10, 10), pady=(10, 10), sticky="news"
        )

        self.quit_button_btn = ttk.Button(
            self.left_frame, text="exit", command=self.root.destroy
        )

        self.quit_button_btn.grid(
            column=0,
            row=0,
            padx=(10, 10),
            pady=(10, 10),
            sticky="s",
        )

        self.adventage1_btn = ttk.Button(
            self.left_frame, text="50:50", command=self.adventage1_func
        )

        self.adventage2_btn = ttk.Button(
            self.left_frame, text="pass it", command=self.adventage2_func
        )

        self.adventage3_btn = ttk.Button(
            self.left_frame, text="double selection", command=self.adventage3_func
        )

        self.adventage1_btn.grid(
            column=0,
            row=2,
            padx=10,
            pady=10,
            sticky="s",
        )

        self.adventage2_btn.grid(
            column=0,
            row=3,
            padx=10,
            pady=10,
            sticky="s",
        )

        self.adventage3_btn.grid(
            column=0,
            row=4,
            padx=10,
            pady=10,
            sticky="s",
        )

        self.leaderboard_toggle_btn = ttk.Button(
            self.left_frame, text="leaderboard", command=self.load_leaderboard
        )

        self.leaderboard_toggle_btn.grid(
            column=0, row=1, padx=(20, 10), pady=(20, 10), sticky="news"
        )

    def adventage1_func(self):
        self.special_skills_states[0] = True

        self.adventage1_btn["state"] = "disabled"

        wrong_answer_buttons = self.wrong_answer_buttons()

        wrong_button1 = wrong_answer_buttons.pop(random.choice(range(3)))

        wrong_button2 = wrong_answer_buttons.pop(random.choice(range(2)))

        wrong_button1["text"] = "removed"

        wrong_button1["state"] = "disabled"

        wrong_button2["text"] = "removed"

        wrong_button2["state"] = "disabled"

    def adventage2_func(self):
        self.special_skills_states[1] = True

        self.adventage2_btn["state"] = "disabled"
        self.update_middle()

    def adventage3_func(self):
        self.special_skills_states[2] = True

        self.adventage3_btn["state"] = "disabled"

    def middle_part(self):
        # self.middle_frame = ttk.LabelFrame(

        #     self.main_frame, text="middle_frame", padding=(20, 20)

        # )

        self.middle_frame = ttk.Frame(self.main_frame, padding=(20, 20))

        self.middle_frame.grid(column=1, row=0, sticky="nsew")

        self.details_frame = ttk.Frame(self.middle_frame)

        self.question_object_text = "subject : {}"

        self.question_object_label = ttk.Label(
            self.details_frame, text=self.question_object_text.format("islam")
        )

        self.content = ttk.Separator(self.details_frame, orient="horizontal")

        self.user_lives_label = ttk.Label(
            self.details_frame,
            text=f"♡{self.user_lives}",
            justify="right",
            font=("Unispace 15 bold"),
        )

        # self.question_frame = ttk.LabelFrame(

        #     self.middle_frame, text="question_frame", padding=(20, 20)

        # )

        self.question_frame = ttk.Frame(self.middle_frame, padding=(20, 20))

        # self.question_frame.grid_columnconfigure(2, weight=1)

        # self.question_frame.grid_rowconfigure(3, weight=1)

        self.question_label = ttk.Label(
            self.question_frame,
            text="""""",
            wraplength=300,
            justify="left",
        )

        self.answers_frame = ttk.Frame(self.middle_frame, padding=(20, 20))

        # self.answers_frame = ttk.Frame(self.middle_frame, padding=(20, 20))

        self.corret_answer = ""

        self.answers_texts = []

        self.answer1_btn = ttk.Button(
            self.answers_frame,
            command=lambda: self.answer_check(self.answer1_btn["text"], 1),  # pyright: ignore[reportAny]
        )

        self.answer2_btn = ttk.Button(
            self.answers_frame,
            command=lambda: self.answer_check(self.answer2_btn["text"], 2),  # pyright: ignore[reportAny]
        )

        self.answer3_btn = ttk.Button(
            self.answers_frame,
            command=lambda: self.answer_check(self.answer3_btn["text"], 3),  # pyright: ignore[reportAny]
        )

        self.answer4_btn = ttk.Button(
            self.answers_frame,
            command=lambda: self.answer_check(self.answer4_btn["text"], 4),  # pyright: ignore[reportAny]
        )

        self.details_frame.grid(row=0, column=1)

        # self.details_frame.grid_columnconfigure(0,weight=1)

        # self.details_frame.grid_rowconfigure(0,weight=1)

        self.question_object_label.grid(row=0, column=0, sticky="w")

        self.content.grid(row=0, column=1, padx=60)

        self.user_lives_label.grid(row=0, column=2, sticky="e")

        self.question_frame.grid(row=1, column=1)

        self.question_label.grid(column=0, row=0)

        self.answers_frame.grid(row=2, column=1, sticky="we")

        self.answer1_btn.grid(row=1, column=0, padx=20, pady=20)

        self.answer2_btn.grid(row=1, column=1, padx=20, pady=20)

        self.answer3_btn.grid(row=2, column=0, padx=20, pady=20)

        self.answer4_btn.grid(row=2, column=1, padx=20, pady=20)

    def select_from_answers(self, answers_texts: list[str]) -> str:
        rand_index = random.choice(range(len(answers_texts)))
        rand_item = answers_texts.pop(rand_index)
        return rand_item

    def answer_check(self, btn_text: str, btn_n: int) -> None:
        if not self.special_skills_states[2]:
            if btn_text == self.corret_answer:
                self.user_rightAnswers += 1
                self.user_point += int(self.current_question_data["difficulty"])
            else:
                self.user_lives -= 1
            self.update_middle()

        else:
            self.special_skills_states[2] = not self.special_skills_states[2]

            if btn_text == self.corret_answer:
                self.user_rightAnswers += 1

                self.user_point += int(self.current_question_data["difficulty"])

            else:
                if btn_n == 1:
                    self.answer1_btn["state"] = "disabled"

                elif btn_n == 2:
                    self.answer2_btn["state"] = "disabled"

                elif btn_n == 3:
                    self.answer3_btn["state"] = "disabled"

                elif btn_n == 4:
                    self.answer4_btn["state"] = "disabled"

    def get_username(self):
        self.root.withdraw()

        self.username_window = Toplevel(self.root)

        self.username_window.title("enter username")

        self.username_window.grab_set()

        self.username_input_label = ttk.Label(
            self.username_window, text="your username : "
        )

        self.username_input = tkinter.Text(self.username_window, height=2, width=10)

        self.user_lives = 3

        def get_username_input() -> None:
            self.username = self.username_input.get(1.0, "end-1c")
            print(self.username)

            self.username_window.grab_release()

            self.root.deiconify()

            self.username_window.destroy()

        def on_closing():
            self.root.destroy()

        self.username_window.protocol("WM_DELETE_WINDOW", on_closing)

        self.username_window_button = ttk.Button(
            self.username_window, text="confirm", command=get_username_input
        )

        self.username_input_label.grid(row=0, column=0)

        self.username_input.grid(row=0, column=1)

        self.username_window_button.grid(row=0, column=2)

    def get_questions_data(self):
        self.questions_data = get_toml_data(QUESTIONS_DATA_FILE)

    def update_middle(self):
        self.update_temp_questions()

        if self.user_lives == 0:
            self.game_over()

        question_lst = list(self.temp["question"])
        question_cnt = len(question_lst)

        if question_cnt == 0:
            self.game_over()
            exit(0)

        if question_cnt > 1:
            randquestion_key: int = random.randint(0, question_cnt - 1)
        else:
            randquestion_key = 0

        self.current_question_data = self.temp["question"].pop(randquestion_key)

        self.corret_answer = self.current_question_data["correct_answer"]

        self.answers_texts = [
            self.current_question_data["correct_answer"],
            self.current_question_data["wrong_answer1"],
            self.current_question_data["wrong_answer2"],
            self.current_question_data["wrong_answer3"],
        ]

        self.answer1_btn["text"] = self.select_from_answers(self.answers_texts)

        self.answer2_btn["text"] = self.select_from_answers(self.answers_texts)

        self.answer3_btn["text"] = self.select_from_answers(self.answers_texts)

        self.answer4_btn["text"] = self.select_from_answers(self.answers_texts)

        self.user_lives_label["text"] = self.user_lives

        self.question_label["text"] = self.current_question_data["question_q"]

        self.question_object_label["text"] = self.question_object_text.format(
            self.current_question_data["subject"]
        )

        self.answer1_btn["state"] = "normal"

        self.answer2_btn["state"] = "normal"

        self.answer3_btn["state"] = "normal"

        self.answer4_btn["state"] = "normal"

    def wrong_answer_buttons(self) -> list[tkinter.Widget]:
        wrong_answer_buttons_list: list[tkinter.Widget] = list()

        # pprint(self.answers_frame.children["!button"]["text"])

        for i in self.answers_frame.children:
            # print(i)

            if self.answers_frame.children[i]["text"] != self.corret_answer:
                wrong_answer_buttons_list.append(self.answers_frame.children[i])

        return wrong_answer_buttons_list

    def update_temp_questions(self):
        # update temp questions data by lookin it asked before if its removes from tem questions

        pprint(self.temp["question"])
        if len(self.temp["question"]) == 0:
            self.min_asked = +1
            for question in self.questions_data["question"]:
                if question is dict:
                    question["ask_time"] = self.min_asked

            self.temp = self.questions_data

        for question in self.temp["question"]:
            if question is dict:
                if question["ask_time"] > self.min_asked:
                    _ = self.temp["question"].pop(question)

    def game_over(self):
        leader_board_data: dict[str, dict[str, str | int]] = dict()
        if os.path.exists(LEARDERBOARD_DATA_FILE):
            leader_board_data = get_toml_data(LEARDERBOARD_DATA_FILE)
        leader_board_data[self.username] = {
            "player": self.username,
            "point": self.user_point,
            "correct": self.user_rightAnswers,
        }
        save_toml_data(LEARDERBOARD_DATA_FILE, leader_board_data)
        self.user_point = 0
        self.user_rightAnswers = 0

        # jokerleri yenilicek

        self.adventage1_btn["state"] = "normal"

        self.adventage2_btn["state"] = "normal"

        self.adventage3_btn["state"] = "normal"

        self.get_username()

    def load_leaderboard(self):
        self.leaderboard_toggle_btn["state"] = "disable"

        self.leaderboard_window = Toplevel(self.root)

        self.leaderboard_window.grab_set()

        self.leaderboard_paned = ttk.Panedwindow(self.leaderboard_window)

        self.leaderboard_paned.grid(
            row=1, column=0, pady=(25, 5), sticky="nsew", rowspan=3
        )

        self.ld_frame = ttk.Frame(self.leaderboard_paned, padding=5)

        self.leaderboard_paned.add(self.ld_frame, weight=1)  # pyright: ignore[reportUnknownMemberType]

        self.ld_scrollbar = ttk.Scrollbar(self.ld_frame)

        self.ld_scrollbar.pack(side="right", fill="y")

        self.leaderboard_treeview = ttk.Treeview(
            self.ld_frame,
            selectmode="browse",
            yscrollcommand=self.ld_scrollbar.set,
            columns=(1, 2),
            height=10,
        )

        # Scrollbar

        self.leaderboard_treeview.pack(expand=True, fill="both")

        _ = self.ld_scrollbar.config(command=self.leaderboard_treeview.yview)  # pyright: ignore[reportUnknownMemberType,reportUnknownArgumentType]
        self.leaderboard_treeview["columns"] = ("player", "correct", "point")
        _ = self.leaderboard_treeview.column("player", anchor="w", width=120)

        _ = self.leaderboard_treeview.column("correct", anchor="w", width=120)

        _ = self.leaderboard_treeview.column("point", anchor="w", width=120)

        self.leaderboard_treeview.heading("player", text="player", anchor="w")

        self.leaderboard_treeview.heading("correct", text="Correct", anchor="w")

        self.leaderboard_treeview.heading("point", text="Point", anchor="w")
        leaderboard_data: dict[str, dict[str, str | int]] = dict()
        if os.path.exists(LEARDERBOARD_DATA_FILE):
            leaderboard_data = get_toml_data(LEARDERBOARD_DATA_FILE)

        for item_index, item_key in enumerate(leaderboard_data):
            _ = self.leaderboard_treeview.insert(
                parent="",
                index=item_index,
                values=(
                    leaderboard_data[item_key]["player"],
                    leaderboard_data[item_key]["correct"],
                    leaderboard_data[item_key]["point"],
                ),
            )  # Open parents

        def on_closing():
            # self.leaderboard_window.grab_release()

            self.leaderboard_window.destroy()

            self.leaderboard_toggle_btn["state"] = "normal"

        self.leaderboard_window.protocol("WM_DELETE_WINDOW", on_closing)


class Test:
    def __init__(self, root: Tk) -> None:
        self.root = root

        self.leaderboard_window = Toplevel(self.root)

        self.leaderboard_window.grab_set()

        self.leaderboard_paned = ttk.Panedwindow(self.leaderboard_window)

        self.leaderboard_paned.grid(
            row=1, column=0, pady=(25, 5), sticky="nsew", rowspan=3
        )

        self.pane_1 = ttk.Frame(self.leaderboard_paned, padding=5)

        _ = self.leaderboard_paned.add(self.pane_1, weight=1)  # pyright: ignore[reportUnknownMemberType]

        self.scrollbar = ttk.Scrollbar(self.pane_1)

        self.scrollbar.pack(side="right", fill="y")

        self.leaderboard_treeview = ttk.Treeview(
            self.pane_1,
            selectmode="browse",
            yscrollcommand=self.scrollbar.set,
            columns=(1, 2),
            height=10,
        )

        # Scrollbar

        self.leaderboard_treeview.pack(expand=True, fill="both")

        _ = self.scrollbar.config(command=self.leaderboard_treeview.yview)  # pyright: ignore[reportUnknownMemberType,reportUnknownArgumentType]

        # Treeview columns

        _ = self.leaderboard_treeview["columns"] = ("player", "correct", "point")

        _ = self.leaderboard_treeview.column("player", anchor="w", width=120)

        _ = self.leaderboard_treeview.column("correct", anchor="w", width=120)

        _ = self.leaderboard_treeview.column("point", anchor="w", width=120)

        self.leaderboard_treeview.heading("player", text="player", anchor="w")

        self.leaderboard_treeview.heading("correct", text="Correct", anchor="w")

        self.leaderboard_treeview.heading("point", text="Point", anchor="w")

        leaderboard_data = get_toml_data(LEARDERBOARD_DATA_FILE)

        for item_index, item_key in enumerate(leaderboard_data):  # pyright: ignore[reportAny]
            _ = self.leaderboard_treeview.insert(
                parent="",
                index=item_index,
                values=(
                    leaderboard_data[item_key]["player"],
                    leaderboard_data[item_key]["correct"],
                    leaderboard_data[item_key]["point"],
                ),
            )  # Open parents

        def on_closing():
            # self.leaderboard_window.grab_release()

            self.leaderboard_window.destroy()

        self.leaderboard_window.protocol("WM_DELETE_WINDOW", on_closing)


def main():
    root = Tk()

    # root.attributes("-fullscreen", True)

    # root.resizable(0, 0)

    # root.minsize(width=1200, height=600)

    # root.maxsize(1200,900)

    # Test(root)

    _ = KnowledgeCompetition(root)

    root.mainloop()
