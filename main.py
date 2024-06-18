from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from random import shuffle
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.word_list = [] 
        layout = FloatLayout()
        
        with layout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=Window.size, pos=layout.pos)

        hello_label = Label(text='환영합니다', font_name='malgun.ttf', font_size='24sp', size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.8}, color=(0, 0, 0, 1))

        study_button = Button(text='학습하기', font_name='malgun.ttf', size_hint=(None, None), size=(100, 50), pos_hint={'center_x': 0.3, 'center_y': 0.5})
        study_button.bind(on_press=self.switch_to_study_screen)

        test_button = Button(text='테스트하기', font_name='malgun.ttf', size_hint=(None, None), size=(100, 50), pos_hint={'center_x': 0.7, 'center_y': 0.5})
        test_button.bind(on_press=self.switch_to_test_screen)

        selfword_button = Button(text='직접 단어 추가하기', font_name='malgun.ttf', size_hint=(None, None), size=(150, 50), pos_hint={'center_x': 0.5, 'center_y': 0.2})
        selfword_button.bind(on_press=self.switch_to_selfword_screen)

        exit_button = Button(text='X', font_name='malgun.ttf', size_hint=(None, None), size=(30, 30), pos_hint={'right': 1, 'top': 1})
        exit_button.background_color = (1, 0, 0, 1)
        exit_button.bind(on_press=App.get_running_app().stop)

        load_button = Button(text='단어 파일 업로드', font_name='malgun.ttf', size_hint=(None, None), size=(150, 50), pos_hint={'center_x': 0.5, 'center_y': 0.3})
        load_button.bind(on_press=self.show_filechooser_and_switch)

        layout.add_widget(hello_label)
        layout.add_widget(study_button)
        layout.add_widget(test_button)
        layout.add_widget(selfword_button)
        layout.add_widget(exit_button)
        layout.add_widget(load_button)

        layout.bind(size=self.update_rect)
        self.add_widget(layout)

    def update_rect(self, instance, value):
        self.rect.size = value

    def switch_to_study_screen(self, instance):
        self.manager.current = 'study_screen'

    def switch_to_test_screen(self, instance):
        self.manager.current = 'test_screen'

    def switch_to_selfword_screen(self, instance):
        self.manager.current = 'self_word_screen'

    def show_filechooser_and_switch(self, instance):
        content = BoxLayout(orientation='vertical')
        self.filechooser = FileChooserListView(filters=['*.txt'])
        content.add_widget(self.filechooser)

        load_button = Button(text='가져오기', font_name='malgun.ttf', size_hint=(1, 0.1))
        load_button.bind(on_press=self.load_file_and_switch)

        content.add_widget(load_button)

        self.popup = Popup(title='파일 선택', content=content, size_hint=(0.9, 0.9))
        self.popup.open()

    def load_file_and_switch(self, instance):
        selection = self.filechooser.selection
        if selection:
            self.current_file = selection[0]
            self.read_file_content()
            self.popup.dismiss()
            self.manager.current = 'file_study_screen'

    def read_file_content(self):
        if self.current_file:
            try:
                with open(self.current_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.word_list = content.splitlines()
                    file_study_screen = self.manager.get_screen('file_study_screen')
                    file_study_screen.set_words(self.word_list)
            except Exception as e:
                print("단어 파일 오류")

                


class FileStudyScreen(Screen):
    def __init__(self, **kwargs):
        super(FileStudyScreen, self).__init__(**kwargs)
        self.words = [""]
        self.current_word_index = 0 
        self.word_label = Label(text=self.words[self.current_word_index], font_name='malgun.ttf', font_size='24sp', size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.6}, color=(0, 0, 0, 1))

        self.layout = FloatLayout()

        with self.layout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=Window.size, pos=self.layout.pos)

        exit_button = Button(text='X', font_name='malgun.ttf', size_hint=(None, None), size=(30, 30), pos_hint={'right': 1, 'top': 1})
        exit_button.background_color = (1, 0, 0, 1)
        exit_button.bind(on_press=App.get_running_app().stop)

        next_button = Button(text='다음', font_name='malgun.ttf', size_hint=(None, None), size=(100, 50), pos_hint={'center_x': 0.5, 'center_y': 0.4})
        next_button.bind(on_press=self.show_next_word)

        self.layout.add_widget(self.word_label)
        self.layout.add_widget(exit_button)
        self.layout.add_widget(next_button)

        self.layout.bind(size=self.update_rect)
        self.add_widget(self.layout)

    def update_rect(self, instance, value):
        self.rect.size = value

    def show_next_word(self, instance):
        self.current_word_index += 1
        if self.current_word_index < len(self.words):
            self.word_label.text = self.words[self.current_word_index]
        else:
            self.word_label.text = "단어학습이 완료되었습니다"
            self.layout.remove_widget(instance)
            self.add_test_button()

    def add_test_button(self):
        test_button = Button(text='테스트하기', font_name='malgun.ttf', size_hint=(None, None), size=(150, 50), pos_hint={'center_x': 0.5, 'center_y': 0.3})
        test_button.bind(on_press=self.switch_to_test_screen)
        self.layout.add_widget(test_button)

    def switch_to_test_screen(self, instance):
        self.manager.current = 'file_test_screen'

    def set_words(self, words):
        self.words = words
        self.current_word_index = 0
        if words:
            self.word_label.text = words[0]

class FileTestScreen(Screen):
    def __init__(self, **kwargs):
        super(FileTestScreen, self).__init__(**kwargs)
        self.words = []
        self.translations = []
        self.current_word_index = 0
        self.correct_answers = 0
        self.incorrect_answers = []

        self.layout = FloatLayout()

        with self.layout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=Window.size, pos=self.layout.pos)

        self.translation_label = Label(text='', font_name='malgun.ttf', font_size='24sp', size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.7}, color=(0, 0, 0, 1))

        self.word_input = TextInput(multiline=False, size_hint=(None, None),font_name='malgun.ttf', size=(200, 50), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        check_button = Button(text='다음', font_name='malgun.ttf', size_hint=(None, None), size=(150, 50), pos_hint={'center_x': 0.5, 'center_y': 0.4})
        check_button.bind(on_press=self.check_answer)

        exit_button = Button(text='X', font_name='malgun.ttf', size_hint=(None, None), size=(30, 30), pos_hint={'right': 1, 'top': 1})
        exit_button.background_color = (1, 0, 0, 1)
        exit_button.bind(on_press=App.get_running_app().stop)

        self.layout.add_widget(self.translation_label)
        self.layout.add_widget(self.word_input)
        self.layout.add_widget(check_button)
        self.layout.add_widget(exit_button)

        self.layout.bind(size=self.update_rect)  

        self.add_widget(self.layout)

    def update_rect(self, instance, value):
        self.rect.size = value  

    def set_words(self, words_and_translations):
        self.words = [word for word, translation in words_and_translations]
        self.translations = [translation for word, translation in words_and_translations]
        self.current_word_index = 0
        self.correct_answers = 0
        self.incorrect_answers = []
        self.translation_label.text = self.translations[self.current_word_index] if self.translations else ""

    def check_answer(self, instance):
        user_answer = self.word_input.text.strip().lower()
        correct_word = self.words[self.current_word_index].lower()
        if user_answer == correct_word:
            self.correct_answers += 1
        else:
            self.incorrect_answers.append((self.translations[self.current_word_index], correct_word, user_answer))
        self.show_next_word()

    def show_next_word(self):
        self.current_word_index += 1
        if self.current_word_index < len(self.words):
            self.translation_label.text = self.translations[self.current_word_index]
            self.word_input.text = ''
        else:
            self.translation_label.text = f"시험이 끝났습니다. 정답 수: {self.correct_answers}/{len(self.words)}"
            self.layout.remove_widget(self.word_input) 
            self.show_incorrect_answers()

    def show_incorrect_answers(self):
        if self.incorrect_answers:
            incorrect_text = "틀린 단어들:\n"
            for translation, correct, user in self.incorrect_answers:
                incorrect_text += f"{translation}: 정답 - {correct}, 답변 - {user}\n"
            incorrect_label = Label(text=incorrect_text, font_name='malgun.ttf', font_size='18sp', size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y':0.5}, color=(1, 0, 0, 1))
            self.layout.add_widget(incorrect_label)

            additional_button = Button(text='오답 공부하기', font_name='malgun.ttf', size_hint=(None, None), size=(150, 50), pos_hint={'center_x': 0.5, 'center_y': 0.3})
            additional_button.bind(on_press=self.switch_to_review_screen)
            self.layout.add_widget(additional_button)
        else:
            no_incorrect_label = Label(text="모든 단어를 맞혔습니다!", font_name='malgun.ttf', font_size='24sp', size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.5}, color=(0, 1, 0, 1))
            self.layout.add_widget(no_incorrect_label)

        for widget in self.layout.children:
            if isinstance(widget, Button) and widget.text == '다음':
                self.layout.remove_widget(widget)

    def switch_to_review_screen(self, instance):
        review_screen = self.manager.get_screen('review_screen')
        review_screen.set_words(self.incorrect_answers)
        self.manager.current = 'review_screen'
        
class SelfWordScreen(Screen):
    def __init__(self, **kwargs):
        super(SelfWordScreen, self).__init__(**kwargs)
        self.words = []
        self.current_word_index = 0
        self.word_label = Label(text='', font_name='malgun.ttf', font_size='24sp', size_hint=(None, None),
                                pos_hint={'center_x': 0.5, 'center_y': 0.6}, color=(0, 0, 0, 1))

        self.words_display = ScrollView(size_hint=(None, None), size=(300, 400), pos_hint={'right': 0.9, 'center_y': 0.5})
        self.words_list_label = Label(text='', font_name='malgun.ttf', font_size='18sp', size_hint_y=None, valign='top',
                                      color=(0, 0, 0, 1))
        self.words_list_label.bind(texture_size=self.words_list_label.setter('size'))
        self.words_display.add_widget(self.words_list_label)

        self.layout = FloatLayout()
        with self.layout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=Window.size, pos=self.layout.pos)

        exit_button = Button(text='X', font_name='malgun.ttf', size_hint=(None, None), size=(30, 30),
                             pos_hint={'right': 1, 'top': 1})
        exit_button.background_color = (1, 0, 0, 1)
        exit_button.bind(on_press=App.get_running_app().stop)

        self.completion_button = Button(text='단어 추가 완료', font_name='malgun.ttf', size_hint=(None, None),
                                        size=(200, 50), pos_hint={'center_x': 0.5, 'center_y': 0.2})
        self.completion_button.bind(on_press=self.show_next_word)

        self.translation_input = TextInput(hint_text='뜻을 입력하세요', font_name='malgun.ttf', size_hint=(None, None),
                                           size=(200, 50), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.word_input = TextInput(hint_text='단어를 입력하세요', font_name='malgun.ttf', size_hint=(None, None),
                                     size=(200, 50), pos_hint={'center_x': 0.5, 'center_y': 0.6})

        self.add_button = Button(text='추가', font_name='malgun.ttf', size_hint=(None, None), size=(100, 50),
                                 pos_hint={'center_x': 0.5, 'center_y': 0.4})
        self.add_button.bind(on_press=self.add_word)

        self.layout.add_widget(self.word_label)
        self.layout.add_widget(self.words_display)
        self.layout.add_widget(exit_button)
        self.layout.add_widget(self.completion_button)
        self.layout.add_widget(self.word_input)
        self.layout.add_widget(self.translation_input)
        self.layout.add_widget(self.add_button)

        self.layout.bind(size=self.update_rect)

        self.add_widget(self.layout)

    def update_rect(self, instance, value):
        self.rect.size = value 

    def add_word(self, instance):
        word = self.word_input.text.strip()
        translation = self.translation_input.text.strip()
        if word and translation:
            self.words.append((word, translation))
            self.word_input.text = ''
            self.translation_input.text = ''
            self.update_words_display()

    def update_words_display(self):
        words_text = ""
        for idx, (word, _) in enumerate(self.words):
            words_text += f"{idx + 1}. {word}\n"
        self.words_list_label.text = words_text

    def show_next_word(self, instance):
        if self.words:
            self.current_word_index += 1
            if self.current_word_index < len(self.words):
                self.word_label.text = self.words[self.current_word_index][0]
            else:
                self.word_label.text = "단어추가가 완료되었습니다"
                self.layout.remove_widget(self.completion_button)
                self.add_test_button()
                self.layout.remove_widget(self.word_input)
                self.layout.remove_widget(self.translation_input)
                self.layout.remove_widget(self.add_button)
        else:
            self.word_input_plz_label = Label(text="먼저 단어를 추가하세요", pos_hint={'center_x': 0.5, 'center_y': 0.8},
                                              font_name='malgun.ttf', color=(1, 0, 0, 1), font_size='30sp')
            self.layout.add_widget(self.word_input_plz_label)

    def add_test_button(self):
        test_button = Button(text='테스트하기', font_name='malgun.ttf', size_hint=(None, None), size=(150, 50),
                             pos_hint={'center_x': 0.5, 'center_y': 0.3})
        test_button.bind(on_press=self.switch_to_test_screen)
        self.layout.add_widget(test_button)

    def switch_to_test_screen(self, instance):
        self.manager.current = 'self_test_screen'
        self.manager.get_screen('self_test_screen').set_words(self.words)

class SelfTestScreen(Screen):
    def __init__(self, **kwargs):
        super(SelfTestScreen, self).__init__(**kwargs)
        self.words = []
        self.translations = []
        self.current_word_index = 0
        self.correct_answers = 0
        self.incorrect_answers = []

        self.layout = FloatLayout()

        with self.layout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=Window.size, pos=self.layout.pos)

        self.translation_label = Label(text='', font_name='malgun.ttf', font_size='24sp', size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.7}, color=(0, 0, 0, 1))

        self.word_input = TextInput(multiline=False, size_hint=(None, None),font_name='malgun.ttf', size=(200, 50), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        check_button = Button(text='다음', font_name='malgun.ttf', size_hint=(None, None), size=(150, 50), pos_hint={'center_x': 0.5, 'center_y': 0.4})
        check_button.bind(on_press=self.check_answer)

        exit_button = Button(text='X', font_name='malgun.ttf', size_hint=(None, None), size=(30, 30), pos_hint={'right': 1, 'top': 1})
        exit_button.background_color = (1, 0, 0, 1)
        exit_button.bind(on_press=App.get_running_app().stop)

        self.layout.add_widget(self.translation_label)
        self.layout.add_widget(self.word_input)
        self.layout.add_widget(check_button)
        self.layout.add_widget(exit_button)

        self.layout.bind(size=self.update_rect)  

        self.add_widget(self.layout)

    def update_rect(self, instance, value):
        self.rect.size = value  

    def set_words(self, words):
        self.words = [word for word, translation in words]
        self.translations = [translation for word, translation in words]
        self.current_word_index = 0
        self.correct_answers = 0
        self.incorrect_answers = []
        self.translation_label.text = self.translations[self.current_word_index] if self.translations else ""

    def check_answer(self, instance):
        user_answer = self.word_input.text.strip().lower()
        correct_word = self.words[self.current_word_index].lower()
        if user_answer == correct_word:
            self.correct_answers += 1
        else:
            self.incorrect_answers.append((self.translations[self.current_word_index], correct_word, user_answer))
        self.show_next_word()

    def show_next_word(self):
        self.current_word_index += 1
        if self.current_word_index < len(self.words):
            self.translation_label.text = self.translations[self.current_word_index]
            self.word_input.text = ''
        else:
            self.translation_label.text = f"시험이 끝났습니다. 정답 수: {self.correct_answers}/{len(self.words)}"
            self.layout.remove_widget(self.word_input) 
            self.show_incorrect_answers()

    def show_incorrect_answers(self):
        if self.incorrect_answers:
            incorrect_text = "틀린 단어들:\n"
            for translation, correct, user in self.incorrect_answers:
                incorrect_text += f"{translation}: 정답 - {correct}, 답변 - {user}\n"
            incorrect_label = Label(text=incorrect_text, font_name='malgun.ttf', font_size='18sp', size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y':0.5}, color=(1, 0, 0, 1))
            self.layout.add_widget(incorrect_label)

            additional_button = Button(text='오답 공부하기', font_name='malgun.ttf', size_hint=(None, None), size=(150, 50), pos_hint={'center_x': 0.5, 'center_y': 0.3})
            additional_button.bind(on_press=self.switch_to_review_screen)
            self.layout.add_widget(additional_button)
        else:
            no_incorrect_label = Label(text="모든 단어를 맞혔습니다!", font_name='malgun.ttf', font_size='24sp', size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.5}, color=(0, 1, 0, 1))
            self.layout.add_widget(no_incorrect_label)

        for widget in self.layout.children:
            if isinstance(widget, Button) and widget.text == '다음':
                self.layout.remove_widget(widget)

    def switch_to_review_screen(self, instance):
        review_screen = self.manager.get_screen('review_screen')
        review_screen.set_words(self.incorrect_answers)
        self.manager.current = 'review_screen'

class StudyScreen(Screen):
    def __init__(self, **kwargs):
        super(StudyScreen, self).__init__(**kwargs)
        self.words = ["absent\n(형) 결석한\n *반: present 출석한", "rude\n(형)무례한\n*반: polite  예의 바른", "adult\n(명) 어른\n*유: grown-up", "begin\n(동) 시작하다\n*유: start", "fail\n(동) 실패하다\n*반: succeed 성공하다"]
        self.current_word_index = 0 
        self.word_label = Label(text=self.words[self.current_word_index], font_name='malgun.ttf', font_size='24sp', size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.6}, color=(0, 0, 0, 1))

        self.layout = FloatLayout()

        with self.layout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=Window.size, pos=self.layout.pos)

        exit_button = Button(text='X', font_name='malgun.ttf', size_hint=(None, None), size=(30, 30), pos_hint={'right': 1, 'top': 1})
        exit_button.background_color = (1, 0, 0, 1)
        exit_button.bind(on_press=App.get_running_app().stop)

        next_button = Button(text='다음', font_name='malgun.ttf', size_hint=(None, None), size=(100, 50), pos_hint={'center_x': 0.5, 'center_y': 0.4})
        next_button.bind(on_press=self.show_next_word)

        self.layout.add_widget(self.word_label)
        self.layout.add_widget(exit_button)
        self.layout.add_widget(next_button)

        self.layout.bind(size=self.update_rect)
        self.add_widget(self.layout)

    def update_rect(self, instance, value):
        self.rect.size = value

    def show_next_word(self, instance):
        self.current_word_index += 1
        if self.current_word_index < len(self.words):
            self.word_label.text = self.words[self.current_word_index]
        else:
            self.word_label.text = "단어학습이 완료되었습니다"
            self.layout.remove_widget(instance)
            self.add_test_button()

    def add_test_button(self):
        test_button = Button(text='테스트하기', font_name='malgun.ttf', size_hint=(None, None), size=(150, 50), pos_hint={'center_x': 0.5, 'center_y': 0.3})
        test_button.bind(on_press=self.switch_to_test_screen)
        self.layout.add_widget(test_button)

    def switch_to_test_screen(self, instance):
        self.manager.current = 'test_screen'

    def set_words(self, words):
        self.words = words
        self.current_word_index = 0
        if words:
            self.word_label.text = words[0]

class TestScreen(Screen):
    def __init__(self, **kwargs):
        super(TestScreen, self).__init__(**kwargs)
        self.words = ["결석한", "무례한", "어른", "시작하다", "실패하다"]  
        self.translations = ["absent", "rude", "adult", "begin", "fail"]  
        self.current_word_index = 0
        self.correct_answers = 0
        self.incorrect_answers = []

        self.layout = FloatLayout()

        with self.layout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=Window.size, pos=self.layout.pos)

        self.word_label = Label(text=self.words[self.current_word_index], font_name='malgun.ttf', font_size='24sp', size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.7}, color=(0, 0, 0, 1))

        self.answer_input = TextInput(multiline=False, size_hint=(None, None), size=(200, 50), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        check_button = Button(text='다음', font_name='malgun.ttf', size_hint=(None, None), size=(150, 50), pos_hint={'center_x': 0.5, 'center_y': 0.4})
        check_button.bind(on_press=self.check_answer)

        exit_button = Button(text='X', font_name='malgun.ttf', size_hint=(None, None), size=(30, 30), pos_hint={'right': 1, 'top': 1})
        exit_button.background_color = (1, 0, 0, 1)
        exit_button.bind(on_press=App.get_running_app().stop)

        self.layout.add_widget(self.word_label)
        self.layout.add_widget(self.answer_input)
        self.layout.add_widget(check_button)
        self.layout.add_widget(exit_button)

        self.layout.bind(size=self.update_rect)
        self.add_widget(self.layout)

        self.randomize_words()

    def update_rect(self, instance, value):
        self.rect.size = value

    def check_answer(self, instance):
        user_answer = self.answer_input.text.strip().lower()
        if self.current_word_index < len(self.translations):
            correct_answer = self.translations[self.current_word_index].lower()
            if user_answer == correct_answer:
                self.correct_answers += 1
            else:
                self.incorrect_answers.append((self.words[self.current_word_index], correct_answer, user_answer))
            self.show_next_word()

    def show_next_word(self):
        self.current_word_index += 1
        if self.current_word_index < len(self.words):
            self.word_label.text = self.words[self.current_word_index]
            self.answer_input.text = ''
        else:
            self.word_label.text = f"시험이 끝났습니다. 정답 수: {self.correct_answers}/{len(self.words)}"
            self.layout.remove_widget(self.answer_input)
            self.show_incorrect_answers()

    def show_incorrect_answers(self):
        if self.incorrect_answers:
            incorrect_text = "틀린 단어들:\n"
            for word, correct, user in self.incorrect_answers:
                incorrect_text += f"{word}: 정답 - {correct}, 답변 - {user}\n"
            incorrect_label = Label(text=incorrect_text, font_name='malgun.ttf', font_size='18sp', size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.5}, color=(1, 0, 0, 1))
            self.layout.add_widget(incorrect_label)

            additional_button = Button(text='오답 공부하기', font_name='malgun.ttf', size_hint=(None, None), size=(150, 50), pos_hint={'center_x': 0.5, 'center_y': 0.3})
            additional_button.bind(on_press=self.switch_to_review_screen)
            self.layout.add_widget(additional_button)
        else:
            no_incorrect_label = Label(text="모든 단어를 맞혔습니다!", font_name='malgun.ttf', font_size='24sp', size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.5}, color=(0, 1, 0, 1))
            self.layout.add_widget(no_incorrect_label)

        for widget in self.layout.children:
            if isinstance(widget, Button) and widget.text == '다음':
                self.layout.remove_widget(widget)

    def switch_to_review_screen(self, instance):
        review_screen = self.manager.get_screen('review_screen')
        review_screen.set_words(self.incorrect_answers)
        self.manager.current = 'review_screen'

    def randomize_words(self):
        combined = list(zip(self.words, self.translations))
        shuffle(combined)
        self.words[:], self.translations[:] = zip(*combined)
        self.word_label.text = self.words[self.current_word_index]

    def set_words(self, words):
        self.words = [word.split('\n')[1]for word in words]  
        self.translations = [word.split('\n')[0] for word in words]  
        self.correct_answers = 0
        self.incorrect_answers = []
        self.randomize_words()

class ReviewScreen(Screen):
    def __init__(self, **kwargs):
        super(ReviewScreen, self).__init__(**kwargs)
        self.words = []
        self.current_word_index = 0
        self.word_label = Label(text='', font_name='malgun.ttf', font_size='24sp', size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.6}, color=(0, 0, 0, 1))

        self.layout = FloatLayout()

        with self.layout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=Window.size, pos=self.layout.pos)

        exit_button = Button(text='X', font_name='malgun.ttf', size_hint=(None, None), size=(30, 30), pos_hint={'right': 1, 'top': 1})
        exit_button.background_color = (1, 0, 0, 1)
        exit_button.bind(on_press=App.get_running_app().stop)

        self.next_button = Button(text='다음', font_name='malgun.ttf', size_hint=(None, None), size=(100, 50), pos_hint={'center_x': 0.5, 'center_y': 0.4})
        self.next_button.bind(on_press=self.show_next_word)

        self.layout.add_widget(self.word_label)
        self.layout.add_widget(exit_button)
        self.layout.add_widget(self.next_button)

        self.layout.bind(size=self.update_rect)
        self.add_widget(self.layout)

    def update_rect(self, instance, value):
        self.rect.size = value

    def show_next_word(self, instance):
        self.current_word_index += 1
        if self.current_word_index < len(self.words):
            self.word_label.text = f"{self.words[self.current_word_index][0]} - {self.words[self.current_word_index][1]}"
        else:
            self.word_label.text = "오답 학습이 완료되었습니다"
            self.layout.remove_widget(self.next_button)
            self.add_review_test_button()

    def add_review_test_button(self):
        self.review_test_button = Button(text='오답 테스트하기', font_name='malgun.ttf', size_hint=(None, None), size=(150, 50), pos_hint={'center_x': 0.5, 'center_y': 0.3})
        self.review_test_button.bind(on_press=self.switch_to_review_test_screen)
        self.layout.add_widget(self.review_test_button)

    def switch_to_review_test_screen(self, instance):
        review_test_screen = self.manager.get_screen('review_test_screen')
        review_test_screen.set_words(self.words)
        self.manager.current = 'review_test_screen'

    def set_words(self, words):
        self.words = words
        self.current_word_index = 0
        if words:
            self.word_label.text = f"{words[0][0]} - {words[0][1]}"
        if hasattr(self, 'review_test_button'):
            self.layout.remove_widget(self.review_test_button)
        if not self.next_button.parent:
            self.layout.add_widget(self.next_button)



class ReviewTestScreen(Screen):
    def __init__(self, **kwargs):
        super(ReviewTestScreen, self).__init__(**kwargs)
        self.words = []
        self.translations = []
        self.current_word_index = 0
        self.correct_answers = 0
        self.incorrect_answers = []

        self.layout = FloatLayout()

        with self.layout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=Window.size, pos=self.layout.pos)

        self.word_label = Label(text='', font_name='malgun.ttf', font_size='24sp', size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.7}, color=(0, 0, 0, 1))

        self.answer_input = TextInput(multiline=False, size_hint=(None, None), size=(200, 50), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        self.check_button = Button(text='다음', font_name='malgun.ttf', size_hint=(None, None), size=(150, 50), pos_hint={'center_x': 0.5, 'center_y': 0.4})
        self.check_button.bind(on_press=self.check_answer)

        exit_button = Button(text='X', font_name='malgun.ttf', size_hint=(None, None), size=(30, 30), pos_hint={'right': 1, 'top': 1})
        exit_button.background_color = (1, 0, 0, 1)
        exit_button.bind(on_press=App.get_running_app().stop)

        self.layout.add_widget(self.word_label)
        self.layout.add_widget(self.answer_input)
        self.layout.add_widget(self.check_button)
        self.layout.add_widget(exit_button)

        self.layout.bind(size=self.update_rect)
        self.add_widget(self.layout)

    def update_rect(self, instance, value):
        self.rect.size = value

    def check_answer(self, instance):
        user_answer = self.answer_input.text.strip().lower()
        if self.current_word_index < len(self.translations):
            correct_answer = self.translations[self.current_word_index]
            if user_answer == correct_answer:
                self.correct_answers += 1
            else:
                self.incorrect_answers.append((self.words[self.current_word_index], correct_answer, user_answer))
            self.show_next_word()

    def show_next_word(self):
        self.current_word_index += 1
        if self.current_word_index < len(self.words):
            self.word_label.text = self.words[self.current_word_index][0]
            self.answer_input.text = ''
        else:
            self.word_label.text = f"시험이 끝났습니다. 정답 수: {self.correct_answers}/{len(self.words)}"
            self.layout.remove_widget(self.answer_input) 
            self.show_incorrect_answers()
                
    def show_incorrect_answers(self):
        if self.incorrect_answers:
            incorrect_text = "틀린 단어들:\n"
            for word, correct, user in self.incorrect_answers:
                incorrect_text += f"{word[0]}: 정답 - {correct}, 답변 - {user}\n"
            incorrect_label = Label(text=incorrect_text, font_name='malgun.ttf', font_size='18sp', size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.5}, color=(1, 0, 0, 1))
            self.layout.add_widget(incorrect_label)
        else:
            no_incorrect_label = Label(text="모든 단어를 맞혔습니다!", font_name='malgun.ttf', font_size='24sp', size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.5}, color=(0, 1, 0, 1))
            self.layout.add_widget(no_incorrect_label)
        for widget in self.layout.children:
            if isinstance(widget, Button) and widget.text == '다음':
                self.layout.remove_widget(widget)

    def set_words(self, words):
        shuffle(words)
        self.words = words
        self.translations = [word[1] for word in words]
        self.current_word_index = 0
        self.correct_answers = 0
        self.incorrect_answers = []
        if words:
            self.word_label.text = words[0][0]
        self.answer_input.text = '' 

class WordStudyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main_screen'))
        sm.add_widget(StudyScreen(name='study_screen'))
        sm.add_widget(TestScreen(name='test_screen'))
        sm.add_widget(ReviewScreen(name='review_screen'))
        sm.add_widget(ReviewTestScreen(name='review_test_screen'))
        sm.add_widget(SelfWordScreen(name='self_word_screen'))
        sm.add_widget(SelfTestScreen(name='self_test_screen'))
        sm.add_widget(FileStudyScreen(name='file_study_screen'))
        sm.add_widget(FileTestScreen(name='file_test_screen'))
        return sm

if __name__ == '__main__':
    WordStudyApp().run()