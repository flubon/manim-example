#!/usr/bin/env python3
from manimlib.imports import *

class Laplace(ThreeDScene):
    def construct(self):
        def regularArrow(theta,phi,scale,text=False):
            phi = phi*DEGREES
            theta = theta*DEGREES
            aX = scale*2*np.cos(theta)*np.cos(phi)
            aY = scale*2*np.cos(theta)*np.sin(phi)
            aZ = scale*2*np.sin(theta)-(scale-1)*np.sqrt(3)
            bX = scale*np.sin(theta)*np.cos(phi)
            bY = scale*np.sin(theta)*np.sin(phi)
            bZ = scale*np.cos(theta)
            force = Line(np.array([aX,aY,aZ]), np.array([aX+bX,aY+bY,aZ-bZ]))
            arrow = Polygon(np.array([aX+bX,aY+bY,aZ-bZ]), np.array([1.01*aX+0.95*bX,1.01*aY+0.95*bY,
                    1.01*aZ-0.95*bZ]), np.array([0.99*aX+0.95*bX,0.99*aY+0.95*bY,0.99*aZ-0.95*bZ]), color=WHITE)
            if text != False:
                text = TextMobject(text)
                text.next_to(arrow,DOWN)
                text.rotate(angle=90*DEGREES,axis=OUT,about_point=np.array([aX+bX,aY+bY,aZ-bZ]))
                text.rotate(angle=90*DEGREES,axis=UP,about_point=np.array([aX+bX,aY+bY,aZ-bZ]))
                return VGroup(force, arrow, text)
            else:
                return VGroup(force, arrow)
        
        balloon = Sphere(radius=2, fill_color=BLUE)
        circle = Circle(radius=1, color=YELLOW).shift(OUT*np.sqrt(3))
        
        self.set_camera_orientation(phi=60*DEGREES, theta=0, distance=20)
        self.play(FadeIn(balloon))
        self.wait()
        part = ParametricSurface(
            lambda u, v: np.array([
                2*np.cos(u)*np.cos(v),
                2*np.cos(u)*np.sin(v),
                2*np.sin(u)
            ]), v_min=0, v_max=TAU, u_min=np.pi/3, u_max=np.pi/2,
            resolution=(2,24)
        )
        self.play(FadeIn(circle))
        self.add(part)
        for n in range(8):
            force = regularArrow(60,45*n,1,"$F$")
            self.add(force)
        self.wait()
        self.play(FadeOut(balloon))
        self.clear()
        
        self.play(part.scale, 3,
            part.shift, OUT*0.3,
            circle.scale, 3
        )
        force = regularArrow(60,270,3, "$F$")
        self.add(force)
        
        conF1 = Line(np.array([0,0,6-2*np.sqrt(3)]),np.array([0,0,3-2*np.sqrt(3)]))
        conF2 = Polygon(np.array([0,0,3-2*np.sqrt(3)]),np.array([0,0.03,3.08-2*np.sqrt(3)]),
                        np.array([0,-0.03,3.08-2*np.sqrt(3)]),color=WHITE)
        conF3 = TextMobject("$F_\\text{合}$")
        conF3.next_to(conF2,DOWN)
        conF3.rotate(angle=90*DEGREES,axis=OUT,about_point=np.array([0,0,3-2*np.sqrt(3)]))
        conF3.rotate(angle=90*DEGREES,axis=UP,about_point=np.array([0,0,3-2*np.sqrt(3)]))
        conF = VGroup(conF1,conF2,conF3)
        self.add(conF)
        
        note = TextMobject("$F$ 为表面张力\\\\$F_\\text{合}$ 为回缩力")
        note.rotate(angle=90*DEGREES,axis=OUT)
        note.rotate(angle=90*DEGREES,axis=UP)
        note.shift(UP*4+IN*2)
        note.scale(2)
        self.play(ShowCreation(note))
        self.wait(2)
        self.play(FadeOut(note))
                
        def showDefault(text,position):
            note = TextMobject(text)
            note.rotate(angle=90*DEGREES,axis=OUT)
            note.rotate(angle=90*DEGREES,axis=UP)
            note.shift(IN*position)
            note.scale(2)
            return note
        formula = showDefault("$$\\boldsymbol{F}_{\\text{合}}=\\oint \\boldsymbol{F}$$",2)
        self.add(formula)
        
        self.play(Rotate(force,angle=360*DEGREES,axis=OUT,about_point=np.array([0,0,np.sqrt(3)])),
                  run_time=6
        )
        self.wait(2)
        
        formula2 = showDefault("$$F_{\\text{合}}=\\pi R\\theta F\\sin\\left(\\frac{1}{2}\\theta\\right)$$",3)
        
        formula3 = showDefault("$$P=\\lim_{\\theta\\to 0}\\frac{\\pi R\\theta F\\sin\\left("+
                               "\\frac{1}{2}\\theta\\right)}{\\pi (\\frac{1}{2}R\\theta)^2}$$",3)
        
        formula4 = showDefault("$$P=\\frac{2F}{R}$$",3)
        
        def angles(theta):
            angle1 = DashedVMobject(Line(np.array([0,0,-2*np.sqrt(3)]),np.array([0,
                                   6*np.sin(theta),6*np.cos(theta)-2*np.sqrt(3)])))
            angle2 = DashedVMobject(Line(np.array([0,0,-2*np.sqrt(3)]),np.array([0,
                                   -6*np.sin(theta),6*np.cos(theta)-2*np.sqrt(3)])))
            angle3 = TextMobject("$\\theta$")
            angle3.scale(2)
            angle3.rotate(angle=90*DEGREES,axis=OUT)
            angle3.rotate(angle=90*DEGREES,axis=UP)
            angle3.next_to(np.array([0,0,-2*np.sqrt(3)]),OUT)
            return VGroup(angle1,angle2,angle3)        

        note1 = showDefault("写成标量形式得：",1)
        angle = angles(30*DEGREES)
        self.play(formula.shift,IN)
        self.add(note1)
        self.play(Transform(formula,formula2))
        self.wait()
        self.remove(note1)
        self.play(FadeOut(formula))
        
        self.play(FadeIn(angle))
        self.play(Indicate(angle))
        self.play(FadeOut(angle),
                  FadeOut(force)
        )
        self.play(FadeIn(formula2))
        
        note2 = showDefault("取面积为零的极限得：",1)
        self.add(note2)
        self.play(Transform(formula2,formula3))
        self.wait()
        self.remove(note2)
        self.play(FadeOut(formula2))
        self.remove(circle)
        for n in range(60,0,-1):
            n = 0.5*n
            circle = Circle(radius=6*np.sin(n*DEGREES), color=YELLOW).shift(OUT*(6*np.cos(n*DEGREES)-2*np.sqrt(3)))
            angle = angles(n*DEGREES)
            self.add(circle,angle)
            self.wait(1/15)
            self.remove(circle,angle)
        self.add(circle,angle)
        self.wait()
        self.play(FadeOut(circle),
                  FadeOut(angle))
        self.play(FadeIn(formula3))

        note3 = showDefault("计算得：",1)
        self.add(note3)
        self.play(Transform(formula3,formula4))
        self.wait()
        self.clear()
        self.play(formula3.shift, 3*OUT,
                  formula3.scale, 3
        )
        self.wait(2)
