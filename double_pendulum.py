from manimlib.imports import *
from numpy import sin, cos
import sympy as sp
import numpy as np

class DoublePendulum(Scene):
    CONFIG = {
        "plane_kwargs" : {
            "color" : RED
            },
        }

    def construct(self):
        plane = NumberPlane(**self.plane_kwargs)
        self.add(plane)
        plane.fade(0.9)
        self.add(plane)

        self.Animation()
        self.wait()
 
    def Animation(self):
        l1 = 4
        l2 = 2.3

        center = np.array([0, 3.5, 0])
        scale_v = 0.5
        scale_w = 0.2

        phi1, phi2, t = sp.symbols('phi1 phi2 t')
        
        phi1 = sp.cos(t)
        phi2 = sp.sin(t)

        x1 = l1 * sp.sin(phi1) + center[0]
        y1 = -l1 * sp.cos(phi1) + center[1]
        x2 = l1 * sp.sin(phi1) + l2 * sp.sin(phi1 + phi2) + center[0]
        y2 = -l1 * sp.cos(phi1) - l2 * sp.cos(phi1 + phi2) + center[1]

        vx1 = sp.diff(x1)
        vy1 = sp.diff(y1)
        vx2 = sp.diff(x2)
        vy2 = sp.diff(y2)

        wx1 = sp.diff(vx1)
        wy1 = sp.diff(vy1)
        wx2 = sp.diff(vx2)
        wy2 = sp.diff(vy2)
        
        x1_func = sp.lambdify(t, x1, "numpy")
        y1_func = sp.lambdify(t, y1, "numpy")
        x2_func = sp.lambdify(t, x2, "numpy")
        y2_func = sp.lambdify(t, y2, "numpy")

        vx1_func = sp.lambdify(t, vx1, "numpy")
        vy1_func = sp.lambdify(t, vy1, "numpy")
        vx2_func = sp.lambdify(t, vx2, "numpy")
        vy2_func = sp.lambdify(t, vy2, "numpy")

        wx1_func = sp.lambdify(t, wx1, "numpy")
        wy1_func = sp.lambdify(t, wy1, "numpy")
        wx2_func = sp.lambdify(t, wx2, "numpy")
        wy2_func = sp.lambdify(t, wy2, "numpy")

        dt = 0.01
        t = np.arange(0.0, 30, dt)
        t[len(t) - 1] = 0.000000001

        p1=VMobject()
        p1.set_points_as_corners([*[[x1_func(t0), y1_func(t0), 0] for t0 in t]])
        p1.make_smooth().set_stroke(None, 2)

        p2=VMobject()
        p2.set_points_as_corners([*[[x2_func(t0), y2_func(t0), 0] for t0 in t]])
        p2.make_smooth().set_stroke(None, 2)

        v1=VMobject()
        v1.set_points_as_corners([*[[vx1_func(t0), vy1_func(t0), 0] for t0 in t]])
        v1.make_smooth().set_stroke(None, 2)

        v2=VMobject()
        v2.set_points_as_corners([*[[vx2_func(t0), vy2_func(t0), 0] for t0 in t]])
        v2.make_smooth().set_stroke(None, 2)

        w1=VMobject()
        w1.set_points_as_corners([*[[wx1_func(t0), wy1_func(t0), 0] for t0 in t]])
        w1.make_smooth().set_stroke(None, 2)

        w2=VMobject()
        w2.set_points_as_corners([*[[wx2_func(t0), wy2_func(t0), 0] for t0 in t]])
        w2.make_smooth().set_stroke(None, 2)

        arrow1 = Arrow()
        arrow1.put_start_and_end_on(p2.get_end(), v2.get_end())
        arrow1.add_updater(lambda m: m.put_start_and_end_on(p2.get_end(),\
                p2.get_end() + v2.get_end() * scale_v))
 
        arrow2 = Arrow()
        arrow2.put_start_and_end_on(p2.get_end(), v2.get_end())
        arrow2.add_updater(lambda m: m.put_start_and_end_on(p1.get_end(),\
                p1.get_end() + v1.get_end() * scale_v))

        arrow5 = Arrow(color=RED)
        arrow5.put_start_and_end_on(p1.get_end(), w1.get_end())
        arrow5.add_updater(lambda m: m.put_start_and_end_on(p1.get_end(),\
                p1.get_end() + w1.get_end() * scale_w))

        arrow6 = Arrow(color=RED)
        arrow6.put_start_and_end_on(p2.get_end(), w2.get_end())
        arrow6.add_updater(lambda m: m.put_start_and_end_on(p2.get_end(),\
                p2.get_end() + w2.get_end() * scale_w))
 
        zero = Dot(color=GREEN)
        zero.move_to(center)
        self.add(zero)

        dot1 = Dot(color=GREEN)
        dot1.move_to(p1.get_end())
        dot1.scale(1.5)
        dot1.add_updater(lambda m: m.move_to(p1.get_end()))

        line1 = Line(center,dot1)
        line1.set_color(PINK)
        self.play(Write(line1))
        line1.add_updater(lambda m: m.become(Line(zero.get_center(),dot1.get_center(),color=PINK)))
        self.add(dot1,line1)

        dot2 = Dot(color=GREEN)
        dot2.scale(2)
        dot2.move_to(p2.get_end())
        dot2.add_updater(lambda m: m.move_to(p2.get_end()))

        line2 = Line(dot1,dot2)
        line2.set_color(YELLOW)
        self.play(Write(line2))
        line2.add_updater(lambda m: m.become(Line(dot1.get_center(),dot2.get_center(),color=YELLOW)))
        self.add(dot2,line2)

        rectangle = Rectangle(color=BLACK, width=4, height=3)
        rectangle.move_to(TOP * 0.5 + 5 * RIGHT)
        self.add(rectangle)

        arrow3 = Arrow()
        arrow3.put_start_and_end_on(TOP * 0.6 + 3 * RIGHT, TOP * 0.6 + 4 * RIGHT)
        v_tex = TexMobject("v_1, v_2")
        v_tex.move_to(TOP * 0.6 + 5 * RIGHT)

        w_tex = TexMobject("w_1, w_2", color=RED)
        w_tex.move_to(TOP * 0.4 + 5 * RIGHT)
        arrow4 = Arrow(color=RED)
        arrow4.put_start_and_end_on(TOP * 0.4 + 3 * RIGHT, TOP * 0.4 + 4 * RIGHT)

        eq1 = TexMobject(r"\varphi_1 = " + sp.latex(phi1))
        eq2 = TexMobject(r"\varphi_2 = " + sp.latex(phi2))
        eq1.move_to(TOP * 0.2 + 5 * RIGHT)
        eq2.move_to(5 * RIGHT)

        self.play(Write(arrow1), Write(arrow2), Write(arrow5), Write(arrow6))
        self.play(Write(arrow3), Write(v_tex))
        self.play(Write(arrow4), Write(w_tex))
        self.play(Write(eq1), Write(eq2))
 
        p1.fade(1)
        p2.fade(1)
        v1.fade(1)
        v2.fade(1)
        w1.fade(1)
        w2.fade(1)

        self.play(ShowCreation(p1), ShowCreation(p2), ShowCreation(v1),\
                ShowCreation(v2), ShowCreation(w1), ShowCreation(w2),\
                rate_func=linear,run_time=30)
