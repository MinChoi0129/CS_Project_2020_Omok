import pygame, time, sys, os
from datetime import datetime

pygame.init()
window = pygame.display.set_mode((800, 600))  # window == 화면 이름
pygame.display.set_caption("오목")


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# 이미지, 사운드 로딩
loading_img = pygame.image.load(resource_path("images/background/loading.png"))
main_bg_img = pygame.image.load(resource_path("images/background/5mok.png"))
back_img = pygame.image.load(resource_path("images/background/HTP_bg.png"))
back_play_img = pygame.image.load(resource_path("images/background/play_back.png"))
start_btn_img = pygame.image.load(resource_path("images/background/start.png"))
rule_btn_img = pygame.image.load(resource_path("images/background/rule.png"))
record_btn_img = pygame.image.load(resource_path("images/background/record.png"))
exit_btn_img = pygame.image.load(resource_path("images/background/exit.png"))
back_btn_img = pygame.image.load(resource_path("images/background/back.png"))
back2_btn_img = pygame.image.load(resource_path("images/background/back2.png"))
see_btn_img = pygame.image.load(resource_path("images/background/see.png"))
table_img = pygame.image.load(resource_path("images/play/table.png"))
output_img = pygame.image.load(resource_path("images/background/output.png"))
s_black_img = pygame.image.load(resource_path("images/play/s_black.png"))
s_white_img = pygame.image.load(resource_path("images/play/s_white.png"))
stateBox_img = pygame.image.load(resource_path("images/state/stateBox.png"))
winner_img = pygame.image.load(resource_path("images/state/winner.png"))
turn_img = pygame.image.load(resource_path("images/state/order.png"))
s_none_img = pygame.image.load(resource_path("images/play/s_blank.png"))
giveup_img = pygame.image.load(resource_path("images/background/giveup.png"))
next_btn_img = pygame.image.load(resource_path("images/play/nextBtn.png"))
gamestart_btn_img = pygame.image.load(resource_path("images/play/startBtn.png"))
gameover_img = pygame.image.load(resource_path("images/state/gameover.png"))
again_btn_img = pygame.image.load(resource_path("images/state/gameover_again.png"))
gomain_btn_img = pygame.image.load(resource_path("images/state/gameover_main.png"))
give_up_img = pygame.image.load(resource_path("images/play/give_up.png"))
yes_img = pygame.image.load(resource_path("images/play/yes.png"))
no_img = pygame.image.load(resource_path("images/play/no.png"))

sounds = [
    resource_path("sounds/water_drop.wav"),
    resource_path("sounds/gamestart_sound.wav"),
    resource_path("sounds/how_to_play_sound.wav"),
    resource_path("sounds/giveup_sound.wav"),
    resource_path("sounds/black_win_sound.wav"),
    resource_path("sounds/white_win_sound.wav"),
    resource_path("sounds/put_black_sound.wav"),
    resource_path("sounds/put_white_sound.wav"),
    resource_path("sounds/choose_daeguk_sound.wav"),
    resource_path("sounds/bgm.ogg")
]

# 전역변수
count = 0  # 수
username1, username2 = "", ""  # 유저1, 유저2
turn = "BLACK"  # 차례(시작 : 흑)
board = [['·' for i in range(19)] for j in range(19)]
evaluationResult = 0  # 0 : 게임진행, 1 : 흑 승리, 2 : 백 승리

class 버튼:  # 완성
    def __init__(self, 윈도우, 버튼이미지, pygame좌표=(0, 0), 실행할함수=None, 매개변수=None, 효과음=(None, 0)):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if pygame좌표[0] + 버튼이미지.get_width() > mouse[0] > pygame좌표[0] and pygame좌표[1] + 버튼이미지.get_height() > mouse[1] > \
                pygame좌표[1]:
            윈도우.blit(버튼이미지, (pygame좌표[0], pygame좌표[1]))
            if click[0]:
                if 효과음[0] != None:
                    pygame.mixer.music.load(효과음[0])
                    pygame.mixer.music.play(효과음[1])
                if 실행할함수 != None:
                    time.sleep(0.5)
                    if 매개변수 != None:
                        실행할함수(매개변수)
                    else:
                        실행할함수()
        else:
            윈도우.blit(버튼이미지, (pygame좌표[0], pygame좌표[1]))


def evaluate(placingAxis):
    global board, evaluationResult, count, turn
    # 현재 게임을 평가하는 메서드
    # game_start 내부에서 사용
    # placingAxis: (list) [x좌표, y좌표] - 착수한 돌의 좌표
    # 내부 변수 x, y는 pygame에서의 그것과 같음
    # 호출 시(placingAxis의 x, y값) game_records에서의 좌표로 호출하면 됨

    try:
        # game_record의 좌표를 pygame의 좌표로 바꾸어서 진행
        x = placingAxis[1]
        y = placingAxis[0]
    except:
        raise Exception

    if turn == "BLACK":
        board[y][x] = '●'
    else:
        board[y][x] = '○'

    count += 1
    turn = "WHITE" if turn == "BLACK" else "BLACK"

    eachLine = ""  # 각 탐색이 끝날 때 마다 빈 문자열로 초기화
    boardSize = len(board)

    # 방금 착수한 돌이 속한 줄만 탐색하면 됨 => 착수한 돌의 좌표값을 필요로 하는 이유
    # 모든 탐색은 각 줄을 문자열로 바꾼 후 패턴을 비교하는 방법을 사용함

    # 가로 탐색
    for i in board[y]:
        eachLine += i
    if eachLine.find("●●●●●") != -1:
        evaluationResult = 1
        return
    elif eachLine.find("○○○○○") != -1:
        evaluationResult = 2
        return

    # 세로 탐색
    eachLine = ""
    for i in range(boardSize):
        eachLine += board[i][x]
    if eachLine.find("●●●●●") != -1:
        evaluationResult = 1
        return
    elif eachLine.find("○○○○○") != -1:
        evaluationResult = 2
        return

    eachLine = ""

    # 대각선 탐색 - '\' 방향
    while x > 0 and y > 0:  # 대각선의 한 쪽 끝까지 이동
        x -= 1
        y -= 1

    for i in range(boardSize):
        if x >= boardSize or y >= boardSize:
            break
        eachLine += board[y][x]
        x += 1
        y += 1

    if eachLine.find("●●●●●") != -1:
        evaluationResult = 1
        return
    elif eachLine.find("○○○○○") != -1:
        evaluationResult = 2
        return

    eachLine = ""
    x = placingAxis[0]
    y = placingAxis[1]

    # 대각선 탐색 - '/' 방향
    while x < boardSize - 1 and y > 0:  # 대각선의 한 쪽 끝까지 이동
        x += 1
        y -= 1

    for i in range(boardSize):
        if x < 0 or y >= boardSize:
            break
        eachLine += board[x][y]
        x -= 1
        y += 1

    if eachLine.find("●●●●●") != -1:
        evaluationResult = 1
        return
    elif eachLine.find("○○○○○") != -1:
        evaluationResult = 2
        return

    # 여기까지 왔다 == 게임 계속 진행
    evaluationResult = 0


def game_over(result):  # GUI화 필요
    global username1, username2
    # result가 1이면 흑 승 / 2이면 백 승
    record_daeguk()

    winner_sound = sounds[4] if result == 1 else sounds[5]
    pygame.mixer.music.load(winner_sound)
    pygame.mixer.music.play(0)

    승자돌그림 = s_black_img if result == 1 else s_white_img
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for x in range(19):
            for y in range(19):
                if board[x][y] == "●":  # 흑
                    y += 1
                    x1 = ((x // 2) * 26 + ((x // 2) - 1) * 25 +
                          69) if x % 2 == 0 else ((x // 2) * 26 + (x // 2) * 25 + 69)
                    y1 = ((y // 2) * 26 + ((y // 2) - 1) * 25 +
                          69) if y % 2 == 0 else ((y // 2) * 26 + (y // 2) * 25 + 69)
                    black_center = s_black_img.get_rect()
                    black_center.center = (y1, x1 + 25)
                    window.blit(s_black_img, black_center)
                elif board[x][y] == "○":  # 백
                    y += 1
                    x1 = ((x // 2) * 26 + ((x // 2) - 1) * 25 +
                          69) if x % 2 == 0 else ((x // 2) * 26 + (x // 2) * 25 + 69)
                    y1 = ((y // 2) * 26 + ((y // 2) - 1) * 25 +
                          69) if y % 2 == 0 else ((y // 2) * 26 + (y // 2) * 25 + 69)
                    white_center = s_white_img.get_rect()
                    white_center.center = (y1, x1 + 25)
                    window.blit(s_white_img, white_center)

        window.blit(stateBox_img, (612, 0))
        window.blit(winner_img, (646, 200))
        window.blit(승자돌그림, (695, 270))
        버튼(window, back2_btn_img, (700, 30), main_menu)
        window.blit(gameover_img, (200, 165))
        버튼(window, again_btn_img, (300, 290), fir_username, 효과음=(sounds[0], 0))
        버튼(window, gomain_btn_img, (300, 350), main_menu, 효과음=(sounds[0], 0))
        pygame.display.update()


def game_start():
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        window.blit(back_img, (0, 0))
        window.blit(table_img, (22, 22))
        window.blit(stateBox_img, (612, 0))
        window.blit(turn_img, (646, 200))
        버튼(window, giveup_img, (700, 30), give_up_btn, 효과음=(sounds[3], 0))

        if turn == "BLACK":
            window.blit(s_black_img, (695, 270))
        else:
            window.blit(s_white_img, (695, 270))

        for x in range(19):
            for y in range(19):
                if board[x][y] == "●":  # 흑
                    y += 1
                    x1 = ((x // 2) * 26 + ((x // 2) - 1) * 25 +
                          69) if x % 2 == 0 else ((x // 2) * 26 + (x // 2) * 25 + 69)
                    y1 = ((y // 2) * 26 + ((y // 2) - 1) * 25 +
                          69) if y % 2 == 0 else ((y // 2) * 26 + (y // 2) * 25 + 69)
                    black_center = s_black_img.get_rect()
                    black_center.center = (y1, x1 + 25)
                    window.blit(s_black_img, black_center)
                elif board[x][y] == "○":  # 백
                    y += 1
                    x1 = ((x // 2) * 26 + ((x // 2) - 1) * 25 +
                          69) if x % 2 == 0 else ((x // 2) * 26 + (x // 2) * 25 + 69)
                    y1 = ((y // 2) * 26 + ((y // 2) - 1) * 25 +
                          69) if y % 2 == 0 else ((y // 2) * 26 + (y // 2) * 25 + 69)
                    white_center = s_white_img.get_rect()
                    white_center.center = (y1, x1 + 25)
                    window.blit(s_white_img, white_center)
                else:
                    y += 1
                    x1 = ((x // 2) * 26 + ((x // 2) - 1) * 25 +
                          69) if x % 2 == 0 else ((x // 2) * 26 + (x // 2) * 25 + 69)
                    y1 = ((y // 2) * 26 + ((y // 2) - 1) * 25 +
                          69) if y % 2 == 0 else ((y // 2) * 26 + (y // 2) * 25 + 69)
                    no_stone_center = s_none_img.get_rect()
                    no_stone_center.center = (y1, x1 + 25)
                    black_or_white = 6 if turn == "BLACK" else 7
                    버튼(window, s_none_img, no_stone_center, evaluate, [x, y - 1], 효과음=(sounds[black_or_white], 0))

        if evaluationResult == 1 or evaluationResult == 2:  # 승자가 가려졌을 경우
            game_over(evaluationResult)
        pygame.display.update()


def main_menu():  # 완성
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        window.blit(main_bg_img, (0, 0))
        버튼(window, start_btn_img, (410, 480), fir_username, 효과음=(sounds[0], 0))
        버튼(window, rule_btn_img, (515, 410), how_to_play, 효과음=(sounds[0], 0))
        버튼(window, record_btn_img, (615, 430), all_daeguks, 효과음=(sounds[0], 0))
        버튼(window, exit_btn_img, (510, 500), quitcmd, 효과음=(sounds[0], 0))
        pygame.display.update()


def give_up_btn():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitcmd()
        window.blit(give_up_img, (50, 200))
        버튼(window, yes_img, (190, 285), give_up, 효과음=(sounds[0], 0))
        버튼(window, no_img, (390, 285), game_start, 효과음=(sounds[0], 0))
        pygame.display.update()


def give_up():
    global evaluationResult
    if turn == 'WHITE':
        evaluationResult = 1
        game_over(1)
    else:
        evaluationResult = 2
        game_over(2)


def how_to_play():  # 완성
    pygame.mixer.music.load(sounds[2])
    pygame.mixer.music.play(0)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        window.blit(back_img, (0, 0))
        font = pygame.font.Font(resource_path('paybooc Bold.ttf'), 20)
        texts = []
        texts.append(font.render("<오목 게임>", True, (255, 212, 0)))
        texts.append(font.render(
            "1. 2명에서 하는 게임으로, 검은색 알을 가진 사람이 먼저 시작한다.", True, (255, 212, 0)))
        texts.append(font.render(
            "2. 알은 선의 교차점에 놓고, 첫 점은 한 가운데에 두는 것이 일반적이다.", True, (255, 212, 0)))
        texts.append(font.render(
            "3. 자기의 알이 양쪽으로 3개 or 4개가 연이어 놓이면 상대방에게 알려준다", True, (255, 212, 0)))
        texts.append(font.render(
            "4. 한 알이 놓이면서 쌍삼(3-3)이 되는 수는 두지 못한다.", True, (255, 212, 0)))
        texts.append(font.render(
            "5. 먼저 자기 알 5개를 가로나 세로, 대각선 중 한 방향으로 연이어 놓는 사람이 승!", True, (255, 212, 0)))

        axis = 80
        for text in texts:
            center = text.get_rect()
            center.center = (400, axis)
            window.blit(text, center)
            axis += 80

        버튼(window, back_btn_img, (700, 30), main_menu, 효과음=(sounds[0], 0))
        pygame.display.update()


def all_daeguks():  # 완성
    pygame.mixer.music.load(sounds[8])
    pygame.mixer.music.play(0)
    file_len = 0
    font = pygame.font.Font(resource_path('paybooc Bold.ttf'), 20)
    
    with open(resource_path("./game_records.txt"), 'r', encoding='utf-8') as f:
        num_of_daeguks = 0
        for i in f:
            num_of_daeguks += 1

    with open(resource_path("./game_records.txt"), 'r', encoding='utf-8') as f:
        contents = list()
        new_contents = list()

        while True:
            content = f.readline()

            if content:
                contents.append(content)
                file_len += 1
            else:
                break

    for j in range(file_len):
        if 'BLACK' in contents[j] or 'WHITE' in contents[j]:
            sep_content = contents[j].split()
            new_contents.append(sep_content)

    new_contents.reverse()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        window.blit(back_img, (0, 0))

        output_index = 0
        output_place = 10

        if num_of_daeguks // 21 > 7:
            for i in range(7):
                버튼(window, see_btn_img, (600, 100 + 60 * i), show_daeguk, i + 1, 효과음=(sounds[0], 0))
                버튼(window, output_img, (150, 100 + 60 * i))
                title = font.render(new_contents[output_index][3] + ' ' + new_contents[output_index]
                [0] + ' VS ' + new_contents[output_index][1], True, (255, 212, 0))
                Title_center = title.get_rect()
                Title_center.center = (350, 115 + output_place)
                window.blit(title, Title_center)
                output_index += 1
                output_place += 60
        else:
            for i in range(num_of_daeguks // 21):
                버튼(window, see_btn_img, (600, 100 + 60 * i), show_daeguk, i + 1, 효과음=(sounds[0], 0))
                버튼(window, output_img, (150, 100 + 60 * i))
                title = font.render(new_contents[output_index][3] + ' ' + new_contents[output_index]
                [0] + ' VS ' + new_contents[output_index][1], True, (255, 212, 0))
                Title_center = title.get_rect()
                Title_center.center = (350, 115 + output_place)
                window.blit(title, Title_center)
                output_index += 1
                output_place += 60

        버튼(window, back_btn_img, (700, 30), main_menu, 효과음=(sounds[0], 0))
        pygame.display.update()


def quitcmd():  # 완성
    pygame.quit()
    sys.exit()


def record_daeguk():  # 완성
    global count, username1, username2, turn, board

    now = datetime.now().strftime('%Y-%m-%d')  # 오늘 날짜
    winner = "WHITE" if turn == "BLACK" else "BLACK"  # 승자

    f = open(resource_path("game_records.txt"), "a+", encoding='utf-8')
    write_data = "%s %s %s %s %d\n" % (
        username1, username2, winner, now, count)  # 유저1 유저2 승자 날짜 n수 기록
    f.write(write_data)

    # 보드 상황 기록
    str_to_write = ""
    for x in range(19):
        for y in range(19):
            str_to_write += (board[x][y] + ' ')
        f.write(str_to_write[:-1] + '\n')
        str_to_write = ""
    f.write('\n')
    f.close()


def show_daeguk(getin):  # 완성
    num_of_daeguks = 0

    with open(resource_path("game_records.txt"), 'r', encoding='utf-8') as f:
        contents = f.readlines()
        for i in contents:
            num_of_daeguks += 1

    num_of_daeguks = num_of_daeguks // 21
    daeguk_number = num_of_daeguks - (getin - 1)

    game_result = []
    g = open(resource_path("game_records.txt"), 'r', encoding='utf-8')
    start_line = 21 * (daeguk_number - 1)
    for i in range(start_line):  # 줄 건너뛰기
        g.readline()

    t = list(g.readline().split())  # 대국 정보(유저1 유저2 승자 날짜 n수)
    game_result.append(t)
    for i in range(19):
        game_result.append(list(g.readline().split()))
    g.close()

    big_font = pygame.font.Font(resource_path('paybooc Bold.ttf'), 30)
    winner_name = game_result[0][0] if game_result[0][2] == "BLACK" else game_result[0][1]
    winner_font = big_font.render(winner_name, True, (0, 0, 0))
    winner_font_center = winner_font.get_rect()
    winner_font_center.center = (706, 340)

    win_count = game_result[0][-1]
    win_count_font = big_font.render(win_count + "수", True, (0, 0, 0))
    win_count_font_center = win_count_font.get_rect()
    win_count_font_center.center = (706, 500)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        window.blit(back_play_img, (0, 0))
        window.blit(stateBox_img, (612, 0))
        window.blit(winner_img, (646, 200))
        window.blit(winner_font, winner_font_center)
        window.blit(win_count_font, win_count_font_center)
        if game_result[0][2] == "BLACK":
            window.blit(s_black_img, (695, 270))
        else:
            window.blit(s_white_img, (695, 270))
        window.blit(table_img, (22, 22))
        for x in range(1, 20):
            for y in range(19):
                if game_result[x][y] == "●":  # 흑
                    y += 1
                    x1 = ((x // 2) * 26 + ((x // 2) - 1) * 25 +
                          69) if x % 2 == 0 else ((x // 2) * 26 + (x // 2) * 25 + 69)
                    y1 = ((y // 2) * 26 + ((y // 2) - 1) * 25 +
                          69) if y % 2 == 0 else ((y // 2) * 26 + (y // 2) * 25 + 69)
                    black_center = s_black_img.get_rect()
                    black_center.center = (y1, x1)
                    window.blit(s_black_img, black_center)
                elif game_result[x][y] == "○":  # 백
                    y += 1
                    x1 = ((x // 2) * 26 + ((x // 2) - 1) * 25 +
                          69) if x % 2 == 0 else ((x // 2) * 26 + (x // 2) * 25 + 69)
                    y1 = ((y // 2) * 26 + ((y // 2) - 1) * 25 +
                          69) if y % 2 == 0 else ((y // 2) * 26 + (y // 2) * 25 + 69)
                    white_center = s_white_img.get_rect()
                    white_center.center = (y1, x1)
                    window.blit(s_white_img, white_center)
        버튼(window, back2_btn_img, (700, 30), all_daeguks, 효과음=(sounds[0], 0))
        pygame.display.update()


def fir_username():
    global count, username1, username2, turn, board, evaluationResult
    count = 0  # 수
    username1, username2 = "", ""  # 유저1, 유저2
    turn = "BLACK"  # 차례(시작 : 흑)
    board = [['·' for i in range(19)] for j in range(19)]
    evaluationResult = 0  # 0 : 게임진행, 1 : 흑 승리, 2 : 백 승리

    font = pygame.font.Font(resource_path('paybooc Bold.ttf'), 25)

    nameTxt = font.render("이름을 7자 이내로 설정하여 주십시오.", True, (255, 212, 0))
    nameTxt_center = nameTxt.get_rect()
    nameTxt_center.center = (400, 260)

    fir_username = '사용자1 이름 : '
    name_input = font.render(fir_username, True, 'white')
    rect1 = name_input.get_rect()
    rect1.topleft = (250, 330)
    cursor = pygame.Rect(rect1.topright, (3, rect1.height))

    def next():
        if len(username1) > 0:
            sec_username()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitcmd()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:  # 글자 지우기
                    if len(fir_username) > 10:
                        fir_username = fir_username[:-1]
                else:  # 글자 입력
                    if len(fir_username) < 17:  # 글자 수 제한
                        fir_username += event.unicode
                name_input = font.render(fir_username, True, 'white')
                rect1.size = name_input.get_size()
                cursor.topleft = rect1.topright
        window.blit(back_play_img, (0, 0))  # 배경 이미지
        window.blit(name_input, rect1)  # 이름 입력창
        window.blit(nameTxt, nameTxt_center)  # 안내 메세지

        if time.time() % 1 > 0.5:  # 커서 깜빡임
            pygame.draw.rect(window, 'white', cursor)
        버튼(window, next_btn_img, (570, 330), next, 효과음=(sounds[0], 0))  # 다음 버튼
        버튼(window, back_btn_img, (700, 30), main_menu, 효과음=(sounds[0], 0))
        username1 = fir_username[10:].strip()
        pygame.display.update()


def sec_username():
    global username2
    font = pygame.font.Font(resource_path('paybooc Bold.ttf'), 25)

    nameTxt = font.render("이름을 7자 이내로 설정하여 주십시오.", True, (255, 212, 0))
    nameTxt_center = nameTxt.get_rect()
    nameTxt_center.center = (400, 260)

    sec_username = '사용자2 이름 : '
    name_input = font.render(sec_username, True, 'white')
    rect1 = name_input.get_rect()
    rect1.topleft = (250, 330)
    cursor = pygame.Rect(rect1.topright, (3, rect1.height))

    def next():
        if len(username2) > 0:
            black_white()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitcmd()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:  # 글자 지우기
                    if len(sec_username) > 10:
                        sec_username = sec_username[:-1]
                else:  # 글자 입력
                    if len(sec_username) < 17:  # 글자 수 제한
                        sec_username += event.unicode
        name_input = font.render(sec_username, True, 'white')
        rect1.size = name_input.get_size()
        cursor.topleft = rect1.topright
        window.blit(back_play_img, (0, 0))  # 배경 이미지
        window.blit(name_input, rect1)  # 이름 입력창
        window.blit(nameTxt, nameTxt_center)  # 안내 메세지

        if time.time() % 1 > 0.5:  # 커서 깜빡임
            pygame.draw.rect(window, 'white', cursor)
        버튼(window, next_btn_img, (570, 330), next, 효과음=(sounds[0], 0))  # 다음 버튼
        버튼(window, back_btn_img, (700, 30), fir_username, 효과음=(sounds[0], 0))
        username2 = sec_username[10:].strip()
        pygame.display.update()


def black_white():
    global username1, username2

    font = pygame.font.Font(resource_path('paybooc Bold.ttf'), 25)
    Txt = font.render(username1 + " 이(가) 흑입니다.", True, (255, 212, 0))
    Txt_center = Txt.get_rect()
    Txt_center.center = (400, 260)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitcmd()
        window.blit(back_play_img, (0, 0))

        버튼(window, gamestart_btn_img, (329, 330), game_start, 효과음=(sounds[1], 0))
        window.blit(Txt, Txt_center)
        pygame.display.update()


window.blit(loading_img, (0, 0))
pygame.display.update()
pygame.mixer.Channel(0).play(pygame.mixer.Sound(sounds[9]))
main_menu()