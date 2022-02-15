from manim import *
import numpy as np
import copy

class Tuzi(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        
        dao = ImageMobject("dao.png").scale(0.6)
        self.add(dao)
        self.wait()
        
        def oneGroupTuzi():
            tuzi = ImageMobject("tuzi.png")
            tuzi.scale(0.4)
            tuzis = []
            for i in range(5):
                tuzis.append(copy.deepcopy(tuzi))
                tuzis[i].move_to(np.array([(i%3-1)/2,i%2/2,0]))
            return Group(*tuzis)
        
        groupsTuzi = [oneGroupTuzi() for _ in range(12)]
        
        ax = Axes(
            x_range = [0, 4],
            y_range = [0, 6.5],
            x_length = 4,
            y_length = 6.5,
            axis_config = { "color": BLACK },
        ).add_coordinates()
        ax.move_to(np.array([4,0,0]))
        graph = [
            ax.plot(lambda x: 1.6 ** x, x_range=[0, 1], color=BLACK),
            ax.plot(lambda x: 1.6 ** x, x_range=[1, 3], color=BLACK)
        ]
        dot = Dot(ax.coords_to_point(1, 1.6), color=RED)
        
        partTex = MathTex(
            r"N_t",
            r"r\times N_t",
            r"r\times r\times\cdots\times N_t",
            r"K",
            color=BLACK
        )
        for i in range(3):
            partTex[i].scale(1.5)
        partTex[0].move_to(np.array([0,2,0]))
        
        self.play(
            FadeIn(groupsTuzi[0]),
            FadeIn(partTex[0])
        )
        self.wait()
        self.play(
            Indicate(partTex[0])
        )
        self.wait(2)
        
        partTex[1].move_to(np.array([-3,3.3,0]))
        self.play(
            *[ApplyMethod(groupsTuzi[i].move_to, np.array([-3,2*(i-1),0]))
            for i in range(3)],
            ApplyMethod(dao.move_to, np.array([-4,0,0])),
            ApplyMethod(partTex[0].move_to, np.array([-4,2,0])),
            Transform(partTex[0], partTex[1]),
            run_time = 2
        )
        
        self.add(ax, graph[0])
        self.play(
            Indicate(partTex[0]),
            Indicate(dot)
        )
        self.wait()
        
        for i in range(3):
            for j in range(4):
                groupsTuzi[4*i+j].move_to(np.array([-3,2*(i-1),0]))
        
        partTex[2].move_to(np.array([-2,3,0]))
        self.play(
            *[ApplyMethod(groupsTuzi[4*i+j].move_to, np.array([j-4,i-1,0]))
            for i in range(3) for j in range(4)],
            Transform(partTex[0], partTex[2])
        )
        self.play(
            Indicate(partTex[0]),
            Create(graph[1]),
            MoveAlongPath(dot, graph[1]),
        )
        self.wait(2)
        
        confine = Circle(radius=1.5, color=BLACK)
        confine.move_to(np.array([-2.5,0,0]))
        self.play(
            FadeIn(confine)
        )
        self.play(
            Indicate(confine)
        )
        self.wait()
        line = Line(np.array([2,1,0]), np.array([6,1,0]), color=BLACK)
        partTex[3].move_to(np.array([-1.5,2,0]))
        self.play(
            FadeIn(line, partTex[3])
        )
        self.play(
            Indicate(line),
            Indicate(partTex[3])
        )
        self.wait()
        self.play(
            FadeOut(line, partTex[3], partTex[0], dao, *groupsTuzi, confine,
                ax, dot, graph[0], graph[1])
        )
        
        maintex = MathTex(
            r"N_{t+1}",
            r"=",
            r"r",
            r"N_t",
            r"\left(1-\frac{N_t}{K}\right)",
            color=BLACK
        ).scale(1.5)
        
        self.play(
            AddTextWordByWord(maintex)
        )
        self.wait()
        self.play(
            Indicate(maintex)
        )
        self.wait()
        
        #28s
        self.play(
            FadeOut(maintex[1], maintex[2], maintex[3], maintex[4]),
            FadeToColor(maintex[0], RED)
        )
        
        maintex[2].set_color(BLUE)
        maintex[3].set_color(ORANGE)
        maintex[4].set_color(GREEN)
        self.play(Indicate(maintex[0]))
        self.play(FadeIn(maintex[3]))
        self.play(Indicate(maintex[3]))
        self.play(FadeIn(maintex[2]))
        self.play(Indicate(maintex[2]))
        self.play(FadeIn(maintex[4]))
        self.play(Indicate(maintex[4]))
        self.play(FadeIn(maintex[1]))
        
        tuziL = [Rectangle(color=RED, height=i, width=1, fill_opacity=1).move_to(np.array([-5,i/2-2,0]))
            for i in [1, 3]]
        xianzhiL = [Rectangle(color=GREEN, height=i, width=1, fill_opacity=1).move_to(np.array([5,i/2-2,0]))
            for i in [4, 2]]
        
        self.play(FadeIn(tuziL[0], xianzhiL[0]))
        self.play(
            Transform(tuziL[0], tuziL[1]),
            Transform(xianzhiL[0], xianzhiL[1]),
            run_time=4
        )
        self.wait()
        self.play(
            FadeOut(maintex, tuziL[0], xianzhiL[0]),
            run_time=2
        )
        
        ax = Axes(
            x_range = [0, 10],
            y_range = [0, 7],
            x_length = 7,
            y_length = 6,
            axis_config={
                "include_numbers": True,
                "color": BLACK,
            },
        )
        
        line1 = ax.plot(lambda x: 3, x_range=[0, 10], color=ORANGE)
        line2 = ax.plot(lambda x: 3*np.sin(x)+3, x_range=[0, 10], color=GREEN)
        self.play(
            FadeIn(ax)
        )
        self.wait()
        self.play(
            Create(line1),
            run_time=3
        )
        self.remove(line1)
        self.play(
            Create(line2),
            run_time=3
        )
        self.play(
            FadeOut(line2)
        )
