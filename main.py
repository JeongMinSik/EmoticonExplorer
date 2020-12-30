from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.graphics import Rectangle, Canvas, Color
import json
import math


X_COUNT = 10


class Emoticon:
    def __init__(self, e_name, e_count):
        self.img = Image(source=f'./images/{e_name}.jpg', size_hint=(1, 0.5))
        self.textures = []
        self.count = e_count
        assert(self.count >= X_COUNT)
        x_count, y_count = X_COUNT, math.ceil(self.count/X_COUNT)
        w = self.img.texture_size[0] / x_count
        h = self.img.texture_size[1] / y_count
        for y in reversed(range(y_count)):
            for x in range(x_count):
                self.textures.append(self.img.texture.get_region(x*w, y*h, w, h))
                if len(self.textures) == self.count:
                    break
        self.reload(0)

    def reload(self, index):
        index = index % len(self.textures)
        self.img.texture = self.textures[index]
        return index


FONT_NAME = 'NanumGothic.ttf'
name_list = [
    ('여자친구!', 'girl', 32),
    ('명MC', 'mc', 24),
    ('묻고 답하기', 'ask_answer', 32),
    ('한국 사람', 'korean', 32),
    ('솔로 완쟈', 'prince', 32),
    ('김대리', 'kim', 24),
    ('무룽v1', 'mooroong_v1', 32),
    ('무룽v2', 'mooroong_v2', 24),
    ('무룽v3', 'mooroong_v3', 24),
    ('움직이는 무룽', 'mooroong_move', 24),
    ('카카오 인턴', 'intern', 24),
    ('튜브 스페셜', 'tube_special', 24),
    ('제이지 스페셜', 'jayg_special', 24),
    ('무지 스페셜', 'muzzi_special', 24),
    ('카카오 캠퍼스', 'campus', 24),
    ('안녕 카카오', 'hi_kakao', 48),
    ('조이풀 데이', 'joyfulday', 24),
    ('니니즈', 'niniz', 48),
    ('카카오 어피치', 'apeach', 24),
    ('카카오 커플', 'couple_kakao', 24),
    ('카카오 페이스', 'kakao_face', 40),
    ('카카오 클래식', 'kakao_classic', 88),
]
keywords = dict()
emoticon_dict = dict()
for title, filename, count in name_list:
    emoticon_dict[title] = Emoticon(filename, count)


class AddLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(AddLayout, self).__init__()

        self.orientation = 'vertical'

        # name_grid
        self.name_grid = GridLayout(cols=3, rows=1, size_hint=(1, 0.3))
        # left button
        left_name_button = Button(text="<-", size_hint=(0.2, 1))
        left_name_button.bind(on_press=self.left_name)
        self.name_grid.add_widget(left_name_button)
        # label
        self.name_label = Label(font_name=FONT_NAME)
        self.name_grid.add_widget(self.name_label)
        # right button
        right_name_button = Button(text="->", size_hint=(0.2, 1))
        right_name_button.bind(on_press=self.right_name)
        self.name_grid.add_widget(right_name_button)

        # emoticon_grid
        self.name_index = 0
        self.emoticon_index = 0
        self.emoticon_grid = self.create_emoticon_grid()

        # tag
        self.input_label = Label(text=f"[{self.emoticon_index+1}/{name_list[self.name_index][2]}]", size_hint=(1, 0.1))
        self.keyword = TextInput(multiline=False, size_hint=(1, 0.1), font_name=FONT_NAME)

        # add button
        self.add = Button(text="등록하기", font_name=FONT_NAME, size_hint=(1, 0.2))
        self.add.bind(on_press=self.add_keyword)

        self.redraw()

    def add_keyword(self, instance):
        global keywords
        key = self.keyword.text
        self.keyword.text = ''
        keywords.setdefault(key, dict())
        emoticon_name = name_list[self.name_index][0]
        keywords[key].setdefault(emoticon_name, set())
        keywords[key][emoticon_name].add(self.emoticon_index)

    def left_emoticon(self, instance):
        emoticon_name = name_list[self.name_index][0]
        curr_emoticon = emoticon_dict[emoticon_name]
        self.emoticon_index = curr_emoticon.reload(self.emoticon_index-1)
        self.input_label.text = f"[{self.emoticon_index+1}/{name_list[self.name_index][2]}]"

    def right_emoticon(self, instance):
        emoticon_name = name_list[self.name_index][0]
        curr_emoticon = emoticon_dict[emoticon_name]
        self.emoticon_index = curr_emoticon.reload(self.emoticon_index+1)
        self.input_label.text = f"[{self.emoticon_index+1}/{name_list[self.name_index][2]}]"

    def left_name(self, instance):
        self.name_index = (self.name_index - 1) % len(name_list)
        emoticon_name = name_list[self.name_index][0]
        curr_emoticon = emoticon_dict[emoticon_name]
        self.emoticon_index = curr_emoticon.reload(0)
        self.input_label.text = f"[{self.emoticon_index+1}/{name_list[self.name_index][2]}]"
        self.redraw()

    def right_name(self, instance):
        self.name_index = (self.name_index + 1) % len(name_list)
        emoticon_name = name_list[self.name_index][0]
        curr_emoticon = emoticon_dict[emoticon_name]
        self.emoticon_index = curr_emoticon.reload(0)
        self.input_label.text = f"[{self.emoticon_index+1}/{name_list[self.name_index][2]}]"
        self.redraw()

    def create_emoticon_grid(self):
        # grid - <- emoticon ->
        emoticon_grid = GridLayout(cols=3, rows=1)
        # left button
        left_button = Button(text="<-")
        left_button.bind(on_press=self.left_emoticon)
        emoticon_grid.add_widget(left_button)
        # emoticon
        e_title = name_list[self.name_index][0]
        curr_emoticon = emoticon_dict[e_title]
        curr_emoticon.img.allow_stretch = True
        emoticon_grid.add_widget(curr_emoticon.img)
        # right button
        right_button = Button(text="->")
        right_button.bind(on_press=self.right_emoticon)
        emoticon_grid.add_widget(right_button)
        # name
        self.name_label.text = f'{e_title} ({self.name_index+1} / {len(name_list)})'

        return emoticon_grid

    def redraw(self):
        self.emoticon_grid.clear_widgets()
        self.clear_widgets()
        self.canvas.clear()
        with self.canvas:
            Color(rgba=[0, 0, 0, 1])
            Rectangle(pos=self.pos, size=self.size)
        self.add_widget(self.name_grid)
        self.emoticon_grid = self.create_emoticon_grid()
        self.add_widget(self.emoticon_grid)
        self.add_widget(self.input_label)
        self.add_widget(self.keyword)
        self.add_widget(self.add)


class SearchLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(SearchLayout, self).__init__()
        self.orientation = 'vertical'

        # message
        self.message = Label(text="검색 창", size_hint=(1, 0.05), font_name=FONT_NAME)
        self.add_widget(self.message)

        # emoticon result
        self.emoticon_box = GridLayout(cols=4)
        self.add_widget(self.emoticon_box)

        # tag
        self.input_label = Label(text="아래 검색 키워드를 입력", size_hint=(1, 0.1), font_name=FONT_NAME)
        self.keyword = TextInput(multiline=False, size_hint=(1, 0.1), font_name=FONT_NAME)
        self.add_widget(self.input_label)
        self.add_widget(self.keyword)

        # search button
        self.search = Button(text="검색하기", font_name=FONT_NAME, size_hint=(1, 0.3))
        self.search.bind(on_press=self.search_keyword)
        self.add_widget(self.search)

    def search_keyword(self, instance):
        idx_dict = keywords.get(self.keyword.text)
        self.emoticon_box.clear_widgets()
        self.keyword.text = ''
        if idx_dict:
            for name, idx_list in idx_dict.items():
                grid = BoxLayout(orientation='horizontal')
                self.emoticon_box.add_widget(Label(text=f'{name} -> ', font_name=FONT_NAME))
                for i in idx_list:
                    img = Image(texture=emoticon_dict[name].textures[i], allow_stretch=True)
                    self.emoticon_box.add_widget(img)
                #self.emoticon_box.add_widget(grid)


class RootWidget(TabbedPanel):
    pass


class RunnerApp(App):
    def __init__(self, **kwargs):
        super(RunnerApp, self).__init__(**kwargs)
        self.font_name = 'NanumGothic.ttf'

    def on_start(self):
        global keywords
        with open('./data.json', 'r', encoding='UTF-8-sig') as f:
            keywords = json.load(f)
            for k, d in keywords.items():
                for emoticon_name, index_list in d.items():
                    keywords[k][emoticon_name] = set(index_list)

    def on_stop(self):
        with open('./data.json', 'w', encoding='UTF-8-sig') as f:
            def serialize_sets(obj):
                if isinstance(obj, set):
                    ll = list(obj)
                    ll.sort()
                    return ll
                return obj
            json.dump(keywords, f, default=serialize_sets, ensure_ascii=False, indent=4, sort_keys=True)

    def build(self):
        return RootWidget()


Builder.load_string("""
<RootWidget>:
    do_default_tab: False

    TabbedPanelItem:
        text: 'search'
        SearchLayout
        
    TabbedPanelItem:
        text: 'add'
        AddLayout
""")


if __name__ == "__main__":
    RunnerApp().run()


