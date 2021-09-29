import math
import pygame

WIDTH, HEIGHT = 1000, 1000
START = (500, 0)
MARGIN = 0.1
K = 3

class Segment:
    def __init__(self, x, y, length):
        self.x = x
        self.y = y
        self.length = length
        self.x2 = self.x
        self.y2 = self.y + length
    def __repr__(self):
        return str((self.x, self.x2)) + str((self.y, self.y2))


def main():
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Inverse Kinematics')
    pygame.init()
    segments = []
    lengths = [100, 200, 100]
    error = sum(lengths)
    backwards = True
    for i in range(K):
        segment = Segment(500, sum(lengths[:i]), lengths[i])
        segments.append(segment)
    approximations = []
    for i in range(K):
        approximations.append((segments[i].x, segments[i].y))
    approximations.append((segments[-1].x2, segments[-1].y2))
    run = True
    while run:
        #print(segments)
        for i in range(K):
            pygame.draw.line(win, (255, 255, 255), (segments[i].x, segments[i].y), (segments[i].x2, segments[i].y2), 5)
            pygame.draw.circle(win, (255, 255, 255), (segments[i].x2, segments[i].y2), 10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                win.fill((0, 0, 0))
                pos = pygame.mouse.get_pos()
                if math.sqrt(math.pow((pos[0] - START[0]), 2) + math.pow((pos[1] - START[1]), 2)) > sum(lengths):
                    print('Out of reach!')
                else:
                    counter = 0
                    while counter < 100 or error > MARGIN:
                        print('Position: ', pos)
                        if backwards:
                            approximations[-1] = pos
                            print(approximations)
                            for i in range(2, K + 1):
                                d = math.sqrt(math.pow(approximations[-i + 1][0] - approximations[-i][0], 2) + math.pow(approximations[-i + 1][1] - approximations[-i][1], 2))
                                approximations[-i] = (approximations[-i + 1][0] - (lengths[-i + 1] * (approximations[-i + 1][0] - approximations[-i][0]) / d), approximations[-i + 1][1] - (lengths[-i + 1] * (approximations[-i + 1][1] - approximations[-i][1]) / d))
                            backwards = False
                        else:
                            approximations[0] = START
                            print(approximations)
                            for i in range(1, K + 1):
                                d = math.sqrt(math.pow(approximations[i - 1][0] - approximations[i][0], 2) + math.pow(approximations[i - 1][1] - approximations[i][1], 2))
                                approximations[i] = (approximations[i - 1][0] - (lengths[i - 1] * (approximations[i - 1][0] - approximations[i][0]) / d), approximations[i - 1][1] - (lengths[i - 1] * (approximations[i - 1][1] - approximations[i][1]) / d))
                            backwards = True
                        for i in range(K):
                            segments[i].x = approximations[i][0]
                            segments[i].y = approximations[i][1]
                            segments[i].x2 = approximations[i + 1][0]
                            segments[i].y2 = approximations[i + 1][1]
                        error = math.sqrt(math.pow(pos[0] - segments[-1].x2, 2) + math.pow(pos[1] - segments[-1].y2, 2))
                        print('Error: ', error)
                        counter += 1
        #win.fill((0, 0, 0))
        pygame.display.update()
    pygame.quit()

if __name__ == '__main__':
    main()
