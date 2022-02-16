from manim import *
import numpy as np
import copy

class Tuzi(Scene):
    def construct(self):
        self.camera.background_color = WHITE
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
        self.play(
            FadeToColor(maintex[2], BLUE)
        )
        
        tex = [copy.deepcopy(maintex[2]), MathTex("=", color = BLACK).scale(2), 
            *[MathTex(str(i), color=BLACK).scale(2) for i in range(2,5)]]
        tex[0].set_color(RED)
        tex[1].move_to(np.array([0,1,0]))
        for i in range(2, 5):
            tex[i].move_to(np.array([0.9,1,0]))
            
        jiantou = ImageMobject("jiantou.png")
        jiantou.move_to(np.array([-0.9,2,0]))
        
        self.play(
            ApplyMethod(tex[0].scale, 2)
        )
        self.play(
            ApplyMethod(tex[0].move_to, np.array([-0.9, 1, 0])),
            ApplyMethod(maintex.move_to, np.array([0, 3, 0])),
            run_time = 2
        )
        self.play(
            FadeIn(tex[1], jiantou, tex[2])
        )
        self.play(
            FadeOut(jiantou)
        )
        #7s up
        
        def pointsOf(ax, r, N0, color=0):
            points = [N0]
            K = 100
            for i in range(19):
                points.append(r*points[i]*(1-points[i]/K))
            if color==0:
                return ax.plot_line_graph(
                    x_values = [i for i in range(20)],
                    y_values = [i/10 for i in points],
                    line_color = RED,
                    vertex_dot_style=dict(stroke_width=2,  fill_color=PURPLE),
                    stroke_width = 2,
                )
            else:
                return ax.plot_line_graph(
                    x_values = [i for i in range(20)],
                    y_values = [i/10 for i in points],
                    line_color = color,
                    vertex_dot_style=dict(stroke_width=1,  fill_color=color),
                    stroke_width = 1,
                )
        
        ax = Axes(
            x_range = [0, 21],
            y_range = [0, 12],
            x_length = 7,
            y_length = 3.5,
            axis_config={
                "include_numbers": True,
                "color": BLACK,
            },
        )
        ax.move_to(np.array([0,-1.5,0]))
        
        
        line = ax.plot(lambda x: 10, x_range=[0, 20], color=ORANGE)
        self.play(FadeIn(ax, line))
        
        for i in range(2,5):
            fig = [pointsOf(ax, i, 5), pointsOf(ax, i, 50), pointsOf(ax, i, 80)]
            for j in range(3):
                self.play(
                    Create(fig[j]),
                    run_time = 2.5
                )
                self.remove(fig[j])
            if i == 3:
                self.add(fig[2])
                self.wait(1.5)
            self.play(FadeOut(fig[2]))
            if i == 4:
                break
            self.play(
                Transform(tex[2], tex[i+1]),
                run_time=2
            )
        fig = [pointsOf(ax, i, 5, RED), pointsOf(ax, i, 50, BLUE), pointsOf(ax, i, 80, ORANGE)]
        self.wait()
        self.play(
            FadeIn(fig[0], fig[1], fig[2])
        )
        self.wait(2)
        self.play(
            Indicate(fig[0]),
            Indicate(fig[1]),
            Indicate(fig[2]),
        )
        self.play(FadeOut(
            ax, *tex[:3], maintex, *fig, line
        ))
        #46s up
