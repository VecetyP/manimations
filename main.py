from manim import *
import numpy as np

class demo(Scene):
    def construct(self):
        t = Text("Hello").shift(UP)
        t2 = Text("World").shift(DOWN)
        self.play(Write(t), Write(t2))
        self.wait(3)


class LaTeXTest(Scene):
    def construct(self):
        tex = MathTex(r"e^{i\pi} + 1 = 0")
        self.play(Write(tex))
        self.wait()


class EulerIdentityNoLatex(Scene):
    def construct(self):

        plane = ComplexPlane(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            background_line_style={
                "stroke_color": BLUE_D,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            }
        ).add_coordinates()
        
        circle = Circle(radius=1, color=YELLOW).set_stroke(opacity=0.5)
        
        theta = ValueTracker(0)
        
        vector = always_redraw(lambda: Vector(
            plane.n2p(np.exp(1j * theta.get_value())),
            color=WHITE
        ))
        
        label = always_redraw(lambda: Text(
            f"e^(i*{theta.get_value():.2f})",
            font_size=24,
            color=WHITE
        ).next_to(vector.get_end(), UR, buff=0.1))

        cos_line = always_redraw(lambda: Line(
            start=plane.n2p(0),
            end=plane.n2p(np.cos(theta.get_value())),
            color=GREEN,
            stroke_width=6
        ))
        
        sin_line = always_redraw(lambda: Line(
            start=plane.n2p(np.cos(theta.get_value())),
            end=plane.n2p(np.cos(theta.get_value()) + 1j * np.sin(theta.get_value())),
            color=RED,
            stroke_width=6
        ))

        formula_text = Text("e^(i*theta) = cos(theta) + i*sin(theta)", font_size=36).to_edge(UP)
        formula_text[12:22].set_color(GREEN)
        formula_text[23:].set_color(RED)

        self.add(plane, circle, formula_text)
        self.play(Create(vector), Write(label))
        self.add(cos_line, sin_line)
        
        self.play(
            theta.animate.set_value(2 * PI),
            run_time=8,
            rate_func=linear
        )
        self.wait(2)


class EulerIdentity(Scene):
    def construct(self):
        # 1. Setup
        plane = ComplexPlane(x_range=[-2, 2, 1], y_range=[-2, 2, 1]).add_coordinates()
        circle = Circle(radius=1, color=YELLOW).set_stroke(opacity=0.5)
        theta = ValueTracker(0)
        
        # 2. Moving parts
        vector = always_redraw(lambda: Vector(
            plane.n2p(np.exp(1j * theta.get_value())),
            color=WHITE
        ))
        
        # Simple label to avoid formatting crashes
        label = always_redraw(lambda: MathTex(
            rf"e^{{i \cdot {theta.get_value():.2f}}}",
            color=WHITE,
            font_size=36
        ).next_to(vector.get_end(), UR, buff=0.1))

        cos_line = always_redraw(lambda: Line(
            plane.n2p(0),
            plane.n2p(np.cos(theta.get_value())),
            color=GREEN, stroke_width=6
        ))
        
        sin_line = always_redraw(lambda: Line(
            plane.n2p(np.cos(theta.get_value())),
            plane.n2p(np.cos(theta.get_value()) + 1j * np.sin(theta.get_value())),
            color=RED, stroke_width=6
        ))

        # 3. Fixed Formula (The fix for your error)
        # We define the formula first, THEN color the parts
        formula = MathTex(r"e^{i\theta} = ", r"\cos(\theta)", r" + ", r"i\sin(\theta)")
        formula.set_color_by_tex(r"\cos(\theta)", GREEN)
        formula.set_color_by_tex(r"i\sin(\theta)", RED)
        formula.to_edge(UP)

        # 4. Animation
        self.add(plane, circle, formula)
        self.play(Create(vector), Write(label))
        self.add(cos_line, sin_line)
        
        self.play(theta.animate.set_value(2 * PI), run_time=10, rate_func=linear)
        self.wait(2)


class FourierTransform(ThreeDScene):
    def construct(self):
        axisXYZ = ThreeDAxes(x_range=[0, 40, 1], y_range=[-10, 10, 1], z_range=[-10, 10, 1], 
                          x_length=20, y_length=10, z_length=20)
        axisXYZ.scale(.5)
        self.wait(1)
        self.play(Create(axisXYZ))

        xz_plane = NumberPlane(
            x_range=[0, 10, 1], 
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 2,
                "stroke_opacity": 0.5
            }
        )

        xz_plane.rotate(90 * DEGREES, axis=RIGHT)
        xz_plane.move_to(axisXYZ.c2p(20, 0, 0))

        self.add(xz_plane)



        time = ValueTracker(0)

        graph = always_redraw(lambda: axisXYZ.plot(lambda x: 
                          np.sin(3*(x - time.get_value()) + 2)*2 +
                          np.sin(2*(x - time.get_value()) + 1)*3 +
                          np.sin(5*(x - time.get_value()) + 3) +
                          np.sin((x - time.get_value()) + 2.5)*2.5 +
                          np.sin(2.5*(x - time.get_value()) + 1.5)*1.5 +
                          np.sin(4*(x - time.get_value()) + 5) +
                          np.sin(4.5*(x - time.get_value()) + 1)*1.5,
                          color=ORANGE))
        self.play(Create(graph))

        self.move_camera(
            phi=-20 * DEGREES,
            run_time=5,
            rate_func=smooth,
            added_anims=[time.animate.set_value(40)]
        )

        sin1 = always_redraw(lambda: axisXYZ.plot(lambda x: np.sin(3*(x - time.get_value()) + 2)*2, color=GREEN).shift(3*OUT))
        sin2 = always_redraw(lambda: axisXYZ.plot(lambda x: np.sin(2*(x - time.get_value()) + 1)*3, color=RED).shift(2*OUT))
        sin3 = always_redraw(lambda: axisXYZ.plot(lambda x: np.sin(5*(x - time.get_value()) + 3), color=YELLOW).shift(1*OUT))
        sin4 = always_redraw(lambda: axisXYZ.plot(lambda x: np.sin((x - time.get_value()) + 2.5)*2.5, color=BLUE))
        sin5 = always_redraw(lambda: axisXYZ.plot(lambda x: np.sin(2.5*(x - time.get_value()) + 1.5)*1.5, color=PURPLE).shift(-1*OUT))
        sin6 = always_redraw(lambda: axisXYZ.plot(lambda x: np.sin(4*(x - time.get_value()) + 5), color=LIGHT_BROWN).shift(-2*OUT))
        sin7 = always_redraw(lambda: axisXYZ.plot(lambda x: np.sin(4.5*(x - time.get_value()) + 1)*1.5, color=PINK).shift(-3*OUT))

        sineGraphs = VGroup(sin7, sin6, sin5, sin4, sin3, sin2, sin1)
        self.play(ReplacementTransform(graph, sineGraphs), run_time=2, rate_func=rush_from)
        self.play(time.animate.set_value(80), run_time=5, rate_func=smooth)


        self.wait(2)


class StreamLine_VectorField(Scene):
    def construct(self):
        plane = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": BLUE_D,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            }
        )

        self.wait(1)

        self.play(Create(plane), run_time=1)

        func = lambda pos: np.sin(pos[0] / 2) * UR + np.cos(pos[1] / 2) * LEFT

        vector_field = ArrowVectorField(
            func,
            x_range=[-7, 7, 1],
            y_range=[-5, 5, 1],
        )

        stream_lines = StreamLines(
            func,
            x_range=[-7, 7, 1],
            y_range=[-5, 5, 1],
            color=BLUE,
            stroke_width=2,
        )

        self.wait(1)

        self.play(Create(vector_field), run_time=1)

        self.add(stream_lines)
        stream_lines.start_animation(warm_up=True, flow_speed=3, time_width=0.8, rate_func=linear)
        self.wait(5)
        self.play(stream_lines.end_animation())
        self.wait(0.5)


class GravityField(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=80 * DEGREES, theta=45 * DEGREES)
        self.move_camera(zoom=0.7)
        axes = ThreeDAxes(
            x_range=[-6, 6, 1],
            y_range=[-6, 6, 1],
            z_range=[-6, 6, 1],
            tips = False,
            axis_config={
                "stroke_color": WHITE,
                "stroke_width": 3,
                "stroke_opacity": 0.8
            }
        )
        self.play(Create(axes))
        planet = Sphere(radius=1, color=BLUE)
        planet.move_to([0, 0, 0])
        self.play(Create(planet))
        self.wait(1)

        gravityfunc = lambda pos: (
            -20 * pos / ((np.linalg.norm(pos) + 1e-6)**3)
            if np.linalg.norm(pos) > 1.0 else np.array([0, 0, 0])
        )

        vector_field = ArrowVectorField(
            gravityfunc,
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            z_range=[-3, 3, 1],
            opacity=0.9,
            vector_config={
                "stroke_width": 3
            }
        )

        self.play(Create(vector_field), run_time=1)

        stream_lines = StreamLines(
            gravityfunc,
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            z_range=[-3, 3, 1],
            color=YELLOW,
            stroke_width=4,
            opacity=0.7
        )

        self.add(stream_lines)
        stream_lines.start_animation(warm_up=True, flow_speed=1, time_width=0.03, rate_func=linear)
        self.wait(1)
        self.begin_ambient_camera_rotation(rate=0.3)
        self.wait(3)
        stream_lines.end_animation()
        self.play(FadeOut(stream_lines))
        self.wait(1)


        #begin the cool orbit stuff
        t = ValueTracker(0)

        def get_grav_func():
            center = planet.get_center()
            return lambda pos: (
                -20 * (pos - center) / ((np.linalg.norm(pos - center) + 0.1)**3)
                if np.linalg.norm(pos - center) > 0.5 else np.array([0, 0, 0])
            )

        planet.add_updater(lambda m: m.move_to([
            2 * np.cos(t.get_value()+PI/2),
            2 * np.sin(t.get_value()),
            np.sin(t.get_value() * 2)
        ]))

        vector_field.add_updater(lambda m: m.become(ArrowVectorField(
            get_grav_func(),
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            z_range=[-3, 3, 1],
            opacity=0.9,
            vector_config={
                "stroke_width": 3
            }
        )))

        self.play(t.animate.set_value(TAU), run_time=6, rate_func=smooth)
        self.stop_ambient_camera_rotation()
        self.wait(1)


class TEST(Scene):
    def construct(self):
        func = lambda pos: (((pos[0] * UR + pos[1] * LEFT) - pos)/4) 
        field = ArrowVectorField(func)
        self.add(field)


class ProjectileMotion(Scene):
    def construct(self):

        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 6, 1],
            x_length=10,
            y_length=6,
            axis_config={"include_tip": True}
        ).add_coordinates()
        
        labels = axes.get_axis_labels(x_label="x", y_label="y")

        plane = NumberPlane(
            x_range=[0, 10, 1],
            y_range=[0, 6, 1],
            x_length=10,
            y_length=6,
            background_line_style={
                "stroke_width": 1,
                "stroke_color": BLUE_D,
                "stroke_opacity": 0.5,
                }
        )
        plane.move_to(axes.c2p(5, 3))



        v0 = 16.0
        theta = 70 * DEGREES
        g = 20
        
        vx = v0 * np.cos(theta)
        vy = v0 * np.sin(theta)
        t_final = (2 * vy) / g


        def get_pos(t):
            x = vx * t
            y = vy * t - 0.5 * g * (t**2)
            return axes.c2p(x, y)

        
        def get_vel_vector(t):
            v_y_current = vy - g * t
            return np.array([vx * 0.3, v_y_current * 0.3, 0])

        
        t_tracker = ValueTracker(0)
        
        
        path = ParametricFunction(
            lambda t: get_pos(t), 
            t_range=[0, t_final], 
            color=YELLOW
        )

        ball = Dot(color=RED).move_to(get_pos(0))
        

        vel_arrow = always_redraw(lambda: Arrow(
            start=ball.get_center(),
            end=ball.get_center() + get_vel_vector(t_tracker.get_value()),
            buff=0,
            color=BLUE,
            stroke_width=4
        ))

        vel_arrow_x = always_redraw(lambda: Arrow(
            start=ball.get_center(),
            end=ball.get_center() + np.array([vx * 0.3, 0, 0]),
            buff=0,
            color=GREEN,
            stroke_width=4
        ))

        vel_arrow_y = always_redraw(lambda: Arrow(
            start=ball.get_center(),
            end=ball.get_center() + np.array([0, (vy - g*t_tracker.get_value())*0.3, 0]),
            buff=0,
            color=RED,
            stroke_width=4
        ))


        pos_formula = MathTex(
            r"\vec{s}(t) = \begin{bmatrix} v_x t \\ v_y t - \frac{1}{2}gt^2 \end{bmatrix}",
            color=YELLOW
        ).scale(0.7).to_corner(UR).shift(LEFT * 0.5)

        vel_formula = MathTex(
            r"\vec{v}(t) = \frac{d\vec{s}}{dt} = \begin{bmatrix} v_x \\ v_y - gt \end{bmatrix}",
            color=BLUE,
        ).scale(0.7).next_to(pos_formula, DOWN, buff=0.5)


        self.play(Write(axes), Write(labels), Write(plane))
        self.play(FadeIn(pos_formula), FadeIn(vel_formula))
        self.add(ball)
        self.play(Create(vel_arrow), Create(vel_arrow_x), Create(vel_arrow_y))
        

        ball.add_updater(lambda m: m.move_to(get_pos(t_tracker.get_value())))


        self.play(
            Create(path),
            t_tracker.animate.set_value(t_final),
            run_time=4,
            rate_func=linear
        )
        
        ball.clear_updaters()
        self.play(FadeOut(vel_arrow), FadeOut(vel_arrow_x), FadeOut(vel_arrow_y), time_width=0.2)
        self.wait(2)



class ProjectileDerivationMath(Scene):
    def construct(self):
        # This will hold our saved boxes at the bottom
        saved_items = VGroup()

        # Helper function to create an explanation + equation line consistently
        def create_line(exp_string, math_string, reference_mob=None):
            exp = Text(exp_string, font_size=20, color=LIGHT_GREY)
            eq = MathTex(math_string, font_size=36)
            line = VGroup(exp, eq).arrange(DOWN, buff=0.2)
            if reference_mob:
                line.next_to(reference_mob, DOWN, buff=0.4)
            return exp, eq, line

        # ==========================================
        # STEP 1: Calculate Gravity
        # ==========================================
        title1 = Text("1. Calculate gravity (A to B)", color=YELLOW, font_size=32).to_edge(UP)
        self.play(Write(title1))

        exp1_1, eq1_1, line1_1 = create_line("Using the kinematic equation:", "v_{yB} = v_{yA} + g \\Delta t", title1)
        self.play(Write(line1_1))
        self.wait(0.8)

        exp1_2, eq1_2, line1_2 = create_line("Substitute known values (apex velocity is 0):", "0 = 98 + g(1.3)", line1_1)
        self.play(Write(line1_2))
        self.wait(0.8)

        exp1_3, eq1_3, line1_3 = create_line("Solve for the gravity constant:", "g = -75.4 \\text{ studs/s}^2", line1_2)
        self.play(Write(line1_3))
        self.wait(1)

        # Box the final value
        box1 = SurroundingRectangle(eq1_3, color=WHITE)
        self.play(Create(box1))
        self.wait(2)

        # Group the box and equation, then fade everything else
        saved_1 = VGroup(eq1_3, box1)
        self.play(
            FadeOut(title1), FadeOut(exp1_1), FadeOut(eq1_1), 
            FadeOut(exp1_2), FadeOut(eq1_2), FadeOut(exp1_3)
        )
        
        # Move the saved value to the bottom left
        self.play(saved_1.animate.scale(0.7).to_edge(DOWN).shift(LEFT * 4))
        saved_items.add(saved_1)

        # ==========================================
        # STEP 2: Total Time A to C
        # ==========================================
        title2 = Text("2. Total time from A to C (T)", color=YELLOW, font_size=32).to_edge(UP)
        self.play(Write(title2))

        exp2_1, eq2_1, line2_1 = create_line("Using the displacement formula:", "\\Delta s = u \\Delta t + \\frac{1}{2} a \\Delta t^2", title2)
        self.play(Write(line2_1))
        self.wait(0.8)

        exp2_2, eq2_2, line2_2 = create_line("Δs = 5,   a = -75.4,   Δt = T,   u = 98:", "5 = 98T + \\frac{1}{2}(-75.4)T^2", line2_1)
        self.play(Write(line2_2))
        self.wait(0.8)

        exp2_3, eq2_3, line2_3 = create_line("Rearrange into a quadratic equation:", "377T^2 - 980T + 50 = 0", line2_2)
        self.play(Write(line2_3))
        self.wait(1)

        box2 = SurroundingRectangle(eq2_3, color=WHITE)
        self.play(Create(box2))
        self.wait(2)

        saved_2 = VGroup(eq2_3, box2)
        self.play(
            FadeOut(title2), FadeOut(exp2_1), FadeOut(eq2_1), 
            FadeOut(exp2_2), FadeOut(eq2_2), FadeOut(exp2_3)
        )
        
        # Move to bottom, next to the first saved value
        self.play(saved_2.animate.scale(0.7).to_edge(DOWN).next_to(saved_1, RIGHT, buff=0.5))
        saved_items.add(saved_2)

        # ==========================================
        # STEP 3: Quadratic Formula
        # ==========================================
        title3 = Text("3. Apply the Quadratic Formula", color=YELLOW, font_size=32).to_edge(UP)
        self.play(Write(title3))

        exp3_1, eq3_1, line3_1 = create_line("Standard quadratic formula:", "x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}", title3)
        self.play(Write(line3_1))
        self.wait(0.8)

        exp3_2, eq3_2, line3_2 = create_line("Substitute a,   b,   c,   and  x:", "T = \\frac{-(-980) \\pm \\sqrt{(-980)^2 - 4(377)(50)}}{2(377)}", line3_1)
        self.play(Write(line3_2))
        self.wait(0.8)

        # Construct line 3 manually so we can split the equation into 3 parts:
        # [0] is "T ="  |  [1] is the messy fraction and 0.05  |  [2] is "2.54"
        exp3_3 = Text("Simplify and select the valid landing time:", font_size=20, color=LIGHT_GREY)
        eq3_3 = MathTex("T = ", "\\frac{490 \\pm 25\\sqrt{354}}{377} \\approx 0.05 , \\; ", "2.54", font_size=36)
        line3_3 = VGroup(exp3_3, eq3_3).arrange(DOWN, buff=0.1).next_to(line3_2, DOWN, buff=0.25)
        
        self.play(Write(line3_3))
        self.wait(0.8)

        # Box ONLY the "2.54" part (which is eq3_3[2]) in GREEN
        box3 = SurroundingRectangle(eq3_3[2], color=GREEN)
        self.play(Create(box3))
        self.wait(2)

        # Create the final clean version to move to the bottom
        final_eq3 = MathTex("T = 2.54 \\text{ s}", font_size=36).move_to(eq3_3)
        final_box3 = SurroundingRectangle(final_eq3, color=WHITE)
        saved_3 = VGroup(final_eq3, final_box3)

        # Clean up the screen: fade out the middle junk, merge 'T =' and '2.54' together
        self.play(
            FadeOut(title3), FadeOut(line3_1), FadeOut(line3_2), FadeOut(exp3_3), 
            FadeOut(eq3_3[1]), # Fades out the fraction and 0.05
            ReplacementTransform(VGroup(eq3_3[0], eq3_3[2]), final_eq3),
            ReplacementTransform(box3, final_box3)
        )
        
        self.play(saved_3.animate.scale(0.7).to_edge(DOWN).next_to(saved_2, RIGHT, buff=0.5))
        saved_items.add(saved_3)

        # ==========================================
        # STEP 4: Time from B to C
        # ==========================================
        title4 = Text("4. Calculate time from B to C", color=YELLOW, font_size=32).to_edge(UP)
        self.play(Write(title4))

        exp4_1, eq4_1, line4_1 = create_line("Subtract ascent time from total time:", "\\Delta t_{B \\to C} = T - t_{A \\to B}", title4)
        self.play(Write(line4_1))
        self.wait(0.8)

        exp4_2, eq4_2, line4_2 = create_line("Substitute calculated values:", "\\Delta t_{B \\to C} = 2.54 - 1.3", line4_1)
        self.play(Write(line4_2))
        self.wait(0.8)

        exp4_3, eq4_3, line4_3 = create_line("Final Answer:", "\\Delta t_{B \\to C} = 1.24 \\text{ s}", line4_2)
        eq4_3.set_color(GREEN)
        self.play(Write(line4_3))
        self.wait(1)

        # Clean the screen one last time, keeping only the final equation
        self.play(
            FadeOut(title4), FadeOut(line4_1), FadeOut(line4_2), FadeOut(exp4_3),
            eq4_3.animate.scale(1.5).move_to(ORIGIN)
        )
        
        # Box and highlight the final answer in the center
        highlight = BackgroundRectangle(eq4_3, color=LIGHT_PINK, fill_opacity=0.2, buff=0.2)
        box4 = SurroundingRectangle(eq4_3, color=RED, buff=0.2)
        self.play(FadeIn(highlight),Create(box4))
        
        self.wait(3)
        
        

class ProjectileVisuals(Scene):
    def construct(self):
        # ==========================================
        # SETUP: Axes, The Curve, and Initial Points
        # ==========================================

        axes = Axes(
            x_range=[-0.2, 3.2, 0.5],
            y_range=[-10, 80, 20],
            x_length=10,
            y_length=5.5,
            axis_config={"color": WHITE, "font_size": 12},
        )
        
        visual_h = 15 
        
        # Function for the curve: y = 98t - 37.7t^2
        def height_func(t): 
            return 98 * t - 37.7 * (t ** 2)

        x_label = axes.get_x_axis_label("Distance")
        y_label = axes.get_y_axis_label("Height (studs)")
        y_label.shift(LEFT * 1.8).shift(UP * 0.15)
        
        # Define Point A (Start) and Point B (Apex)
        pt_A = axes.coords_to_point(0, 0)
        pt_B = axes.coords_to_point(1.3, height_func(1.3))
        pt_C = axes.coords_to_point(2.44, visual_h)
        
        
        landing_box = Rectangle(
            width=1.5, 
            height=0.9, 
            fill_opacity=0.5, 
            fill_color=GREY, 
            color=WHITE
        )
        # Position the box so its TOP surface is exactly at pt_C
        # pt_C was defined at (2.44, visual_h)
        landing_box.move_to(pt_C, aligned_edge=UP).shift(RIGHT*0.6)

        self.play(Create(axes), run_time=1)
        self.play(Write(x_label), Write(y_label), run_time=1.5)
        self.play(FadeIn(landing_box))
        # ---> THE ACTUAL CURVE <---
        graph = axes.plot(height_func, color=BLUE, x_range=[0, 2.44])
        self.play(Create(graph), run_time=2)


        dot_A = Dot(pt_A, color=GREEN)
        label_A = Text("A", font_size=24).next_to(dot_A, DL)
        
        dot_B = Dot(pt_B, color=RED)
        label_B = Text("B (Apex)", font_size=24).next_to(dot_B, UP)

        # ==========================================
        # UPDATED VISUAL STEP 1: Motion from A to B with Vectors
        # ==========================================
        # 1. Show Point A and its initial vertical velocity
        v_y_initial_text = MathTex("v_{yA} = 98", font_size=24, color=GREEN).next_to(dot_A, LEFT, buff=0.3).shift(UP * 0.4)
        self.play(FadeIn(dot_A, label_A), Write(v_y_initial_text))
        self.wait(0.8)

        # 2. Setup the moving parts
        t_tracker = ValueTracker(0)

        # Helper function for vertical velocity
        def get_vy(t):
            return 98 - 75.4 * t

        # Arbitrary horizontal speed for the visual arc
        vx_val = 1.5 

        # The moving point
        moving_dot = always_redraw(lambda: Dot(
            axes.coords_to_point(t_tracker.get_value(), height_func(t_tracker.get_value())),
            color=WHITE
        ))

        # Vertical velocity arrow (scaled down by 30 so it fits nicely on screen)
        vy_arrow = always_redraw(lambda: Arrow(
            moving_dot.get_center(),
            moving_dot.get_center() + UP * (get_vy(t_tracker.get_value()) / 30),
            buff=0, color=GREEN, stroke_width=4, max_tip_length_to_length_ratio=0.2
        ))

        # Horizontal velocity arrow
        vx_arrow = always_redraw(lambda: Arrow(
            moving_dot.get_center(),
            moving_dot.get_center() + RIGHT * vx_val,
            buff=0, color=RED, stroke_width=4, max_tip_length_to_length_ratio=0.2
        ))
        
        vy_arrow_fixed = Arrow(
            moving_dot.get_center(),
            moving_dot.get_center() + UP * (get_vy(t_tracker.get_value()) / 30),
            buff=0, color=GREEN, stroke_width=4, max_tip_length_to_length_ratio=0.2
        )
        
        vx_arrow_fixed = Arrow(
            moving_dot.get_center(),
            moving_dot.get_center() + RIGHT * vx_val,
            buff=0, color=RED, stroke_width=4, max_tip_length_to_length_ratio=0.2
        )

        # Dynamic text tracking the current v_y
        vy_dynamic_text = always_redraw(lambda: MathTex(
            f"v_y = {max(0, get_vy(t_tracker.get_value())):.1f}", font_size=20, color=GREEN
        ).next_to(vy_arrow, UP, buff=0.1))

        self.play(FadeIn(moving_dot), FadeIn(vy_dynamic_text), FadeIn(vy_arrow), FadeIn(vx_arrow), FadeIn(vy_arrow_fixed), FadeIn(vx_arrow_fixed))

        # 3. Animate the flight to the apex (t=1.3)
        self.play(t_tracker.animate.set_value(1.3), run_time=3, rate_func=linear)
        self.remove(vy_dynamic_text)
        self.wait(0.5)

        # 4. Show Point B, its final vertical velocity, AND the t=1.3 line
        v_y_final_text = MathTex("v_{yB} = 0", font_size=24, color=GREEN).next_to(dot_B, UP * 1.1, buff=0.7)
        
        t_B_line = axes.get_vertical_line(pt_B, color=YELLOW, line_func=DashedLine)
        t_B_label = MathTex("t = 1.3", font_size=24).next_to(axes.coords_to_point(1.3, 0), DOWN)

        # Fade out the dynamic text, show the final v_y, and drop the dashed line down to the axis
        self.play(
            FadeIn(dot_B, label_B), 
            Write(v_y_final_text),
            Create(t_B_line),
            Write(t_B_label)
        )
        self.wait(0.8)
        
        vinitialBox = SurroundingRectangle(v_y_initial_text, color=WHITE, fill_opacity=0.1)
        vfinalBox = SurroundingRectangle(v_y_final_text, color=WHITE, fill_opacity=0.1)
        timeBox = SurroundingRectangle(t_B_label, color=WHITE, fill_opacity=0.1)
        self.play(Create(vinitialBox), Create(vfinalBox), Create(timeBox), run_time=1)
        self.wait(1)

        # 5. Show the math calculation to find g
        calc_group = VGroup(
            MathTex("\\Delta v_y = v_{yB} - v_{yA} = 0 - 98 = -98", font_size=24),
            MathTex("\\Delta t = 1.3 \\text{ s}", font_size=24),
            MathTex("g = \\frac{\\Delta v_y}{\\Delta t} = \\frac{-98}{1.3} = -75.4 \\text{ studs/s}^2", font_size=28, color=YELLOW)
        ).arrange(DOWN, buff=0.2).to_corner(UR, buff=0.5)

        calc_box = SurroundingRectangle(calc_group, color=WHITE, fill_opacity=0.1)

        self.play(Write(calc_group), run_time=3)
        self.wait(1)
        self.play(Create(calc_box), run_time=1)
        self.wait(3)

        # 6. Clean up the screen to prepare for Step 2
        # Notice we DO NOT fade out t_B_line or t_B_label here, so they stay for the brace later!
        self.play(
            FadeOut(moving_dot), FadeOut(vx_arrow), FadeOut(vy_arrow),
            FadeOut(v_y_initial_text), FadeOut(v_y_final_text),
            FadeOut(calc_group), FadeOut(calc_box),
            FadeOut(vinitialBox), FadeOut(vfinalBox), FadeOut(timeBox),
            FadeOut(vx_arrow_fixed), FadeOut(vy_arrow_fixed)
        )
        self.wait(0.5)
        

        # ==========================================
        # VISUAL STEP 2 & 3: The "Middle Ground" y=15 line
        # ==========================================
        
        h_tracker = ValueTracker(0) # Starts at y=0

        # 1. The moving pink line
        y5_line = always_redraw(lambda: axes.get_horizontal_line(
            axes.coords_to_point(2.4, h_tracker.get_value()), 
            color=PINK, 
            line_func=DashedLine
        ))

        # 2. The Highlight Area (The "Space Underneath")
        # We use a Rectangle that grows as the tracker increases
        dy_highlight = always_redraw(lambda: Rectangle(
            width=axes.coords_to_point(2.4, 0)[0] - axes.coords_to_point(0, 0)[0],
            height=abs(axes.coords_to_point(0, h_tracker.get_value())[1] - axes.coords_to_point(0, 0)[1]),
            fill_color=PINK,
            fill_opacity=0.2,
            stroke_width=0
        ).move_to(axes.coords_to_point(0, 0), aligned_edge=DL))

        # 3. The Dynamic Label (Counts from 0 to 5)
        y5_label = always_redraw(lambda: MathTex(
            # We divide by 3 to map the visual_h (15) back to the math value (5)
            f"\\Delta y = {h_tracker.get_value() / 3:.1f}", 
            color=PINK, 
            font_size=24
        ).next_to(axes.coords_to_point(0, h_tracker.get_value()), LEFT, buff=0.2))

        # Show second root (Point C) (labeled as math result 2.54)
        dot_C = Dot(pt_C, color=GREEN)
        label_C = Text("C", font_size=24).next_to(dot_C, UR, buff=0.1)

        # --- ANIMATION ---
        self.play(FadeIn(dy_highlight, y5_line, y5_label, dot_C, label_C))
        
        
        # Move from 0 to 15 (visual_h)
        self.play(h_tracker.animate.set_value(visual_h), run_time=2, rate_func=smooth)
        self.wait(1)

        # Coordinates solved to sit perfectly on the curve at y=15
        pt_root1 = axes.coords_to_point(0.16, visual_h) 

        dot_root1 = Dot(pt_root1, color=YELLOW)
        
        
        # Show first root (labeled as math result 0.05)
        self.play(FadeIn(dot_root1))
        root1_label = MathTex("t \\approx 0.05", font_size=20).next_to(dot_root1, UP)
        self.play(Write(root1_label))


        root2_label = MathTex("T = 2.54", font_size=30, color=GREEN).next_to(label_C, RIGHT, buff=0.2)
        self.play(Write(root2_label))
        self.wait(1)

        self.play(FadeOut(dot_root1), FadeOut(root1_label))

        # ==========================================
        # VISUAL STEP 4: Time from B to C (The Brace)
        # ==========================================
        # Connect apex (1.3) to our visual Point C (2.44)
        brace = BraceBetweenPoints(
            axes.coords_to_point(1.3, 0), 
            axes.coords_to_point(2.44, 0), 
            direction=DOWN, 
            color=ORANGE
        )
        brace.shift(DOWN*0.5)
        brace_text = brace.get_tex("\\Delta t = 1.24\\text{ s}").scale(0.8)
        
        self.play(FadeIn(brace), Write(brace_text))
        
        # Highlight final segment from Apex to Point C
        arc_segment = axes.plot(height_func, color=ORANGE, x_range=[1.3, 2.44])
        self.play(Create(arc_segment), run_time=1.5)
        self.wait(2)
        


class ProductRuleProof(Scene):
    def construct(self):
        # ── 0. Title ────────────────────────────────────────────────────────
        title = Text("Product Rule", font_size=52, weight=BOLD)
        subtitle = MathTex(r"\frac{d}{dx}[f(x)\,g(x)] = f'(x)\,g(x) + f(x)\,g'(x)",
                           font_size=36)
        subtitle.next_to(title, DOWN, buff=0.4)

        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(subtitle, shift=UP * 0.3))
        self.wait(1.2)
        self.play(FadeOut(title), FadeOut(subtitle))

        # ── 1. Setup: idea text ─────────────────────────────────────────────
        idea = Text("Think of f and g as side lengths of a rectangle.",
                    font_size=28, color=YELLOW)
        idea.to_edge(UP)
        self.play(FadeIn(idea))
        self.wait(0.8)

        # ── 2. Draw the original rectangle  f × g ───────────────────────────
        # We'll use ValueTrackers so the rectangle can grow later.
        f_val = ValueTracker(2.5)   # initial f
        g_val = ValueTracker(1.8)   # initial g
        df_val = ValueTracker(0.0)  # Δf  (animated to 0.7)
        dg_val = ValueTracker(0.0)  # Δg  (animated to 0.5)

        SCALE = 1.4          # pixel scale factor
        ORIGIN = LEFT * 3.5 + DOWN * 1.2

        def make_rect(w, h, color, opacity=1.0):
            r = Rectangle(width=w * SCALE, height=h * SCALE,
                          color=color, fill_color=color, fill_opacity=opacity)
            r.move_to(ORIGIN, aligned_edge=DL)
            return r

        # Main (original) rectangle — blue
        main_rect = always_redraw(lambda: make_rect(
            f_val.get_value(), g_val.get_value(), BLUE, opacity=0.35))

        # Brace + labels for sides
        f_brace = always_redraw(lambda: Brace(
            make_rect(f_val.get_value(), g_val.get_value(), WHITE, 0),
            direction=DOWN, buff=0.12, color=WHITE))
        g_brace = always_redraw(lambda: Brace(
            make_rect(f_val.get_value(), g_val.get_value(), WHITE, 0),
            direction=LEFT, buff=0.12, color=WHITE))

        f_label = always_redraw(lambda: MathTex("f", color=WHITE, font_size=32)
                                .next_to(f_brace, DOWN, buff=0.15))
        g_label = always_redraw(lambda: MathTex("g", color=WHITE, font_size=32)
                                .next_to(g_brace, LEFT, buff=0.15))

        area_label = always_redraw(lambda: MathTex("A = fg", font_size=30,
                                                    color=BLUE_B)
                                   .move_to(ORIGIN + RIGHT * f_val.get_value()
                                            * SCALE / 2
                                            + UP * g_val.get_value()
                                            * SCALE / 2))

        self.play(FadeIn(idea))
        self.play(Create(main_rect), run_time=0.8)
        self.play(GrowFromCenter(f_brace), GrowFromCenter(g_brace))
        self.play(Write(f_label), Write(g_label), Write(area_label))
        self.wait(0.8)

        # ── 3. Transition text ───────────────────────────────────────────────
        self.play(FadeOut(idea))
        step1 = Text("Now increase f by Δf and g by Δg …",
                     font_size=26, color=YELLOW).to_edge(UP)
        self.play(FadeIn(step1))

        # ── 4. Δg strip (top, GREEN) ─────────────────────────────────────────
        dg_rect = always_redraw(lambda: Rectangle(
            width=f_val.get_value() * SCALE,
            height=dg_val.get_value() * SCALE,
            color=GREEN, fill_color=GREEN, fill_opacity=0.55
        ).move_to(ORIGIN + UP * g_val.get_value() * SCALE, aligned_edge=DL))

        # Δf strip (right, RED)
        df_rect = always_redraw(lambda: Rectangle(
            width=df_val.get_value() * SCALE,
            height=g_val.get_value() * SCALE,
            color=RED, fill_color=RED, fill_opacity=0.55
        ).move_to(ORIGIN + RIGHT * f_val.get_value() * SCALE, aligned_edge=DL))

        # Corner piece (PURPLE) — Δf·Δg
        corner_rect = always_redraw(lambda: Rectangle(
            width=df_val.get_value() * SCALE,
            height=dg_val.get_value() * SCALE,
            color=PURPLE, fill_color=PURPLE, fill_opacity=0.75
        ).move_to(ORIGIN
                  + RIGHT * f_val.get_value() * SCALE
                  + UP * g_val.get_value() * SCALE,
                  aligned_edge=DL))

        self.play(FadeIn(dg_rect), FadeIn(df_rect), FadeIn(corner_rect))

        # Animate the strips growing
        self.play(
            df_val.animate.set_value(0.7),
            dg_val.animate.set_value(0.5),
            run_time=1.8, rate_func=smooth
        )
        self.wait(0.5)

        # ── 5. Label the three new pieces ───────────────────────────────────
        dg_lbl = always_redraw(lambda: MathTex(r"f\,\Delta g", font_size=26,
                                                color=GREEN)
                               .move_to(ORIGIN
                                        + RIGHT * f_val.get_value() * SCALE / 2
                                        + UP * (g_val.get_value()
                                                + dg_val.get_value() / 2)
                                        * SCALE))

        df_lbl = always_redraw(lambda: MathTex(r"\Delta f\,g", font_size=26,
                                                color=RED)
                               .move_to(ORIGIN
                                        + RIGHT * (f_val.get_value()
                                                   + df_val.get_value() / 2)
                                        * SCALE
                                        + UP * g_val.get_value() * SCALE / 2))

        corner_lbl = always_redraw(lambda: MathTex(r"\Delta f\,\Delta g",
                                                    font_size=20, color=PURPLE)
                                   .move_to(ORIGIN
                                            + RIGHT * (f_val.get_value()
                                                       + df_val.get_value() / 2)
                                            * SCALE
                                            + UP * (g_val.get_value()
                                                    + dg_val.get_value() / 2)
                                            * SCALE))

        self.play(Write(dg_lbl), Write(df_lbl), Write(corner_lbl))
        self.wait(1)

        # ── 6. Algebra panel on the right ────────────────────────────────────
        self.play(FadeOut(step1))
        step2 = Text("Total change in area:", font_size=26,
                     color=YELLOW).to_edge(UP)
        self.play(FadeIn(step2))

        eq1 = MathTex(r"\Delta A", "=",
                      r"\underbrace{f\,\Delta g}_{\text{green}}",
                      "+",
                      r"\underbrace{\Delta f\,g}_{\text{red}}",
                      "+",
                      r"\underbrace{\Delta f\,\Delta g}_{\text{purple}}",
                      font_size=28)
        eq1.set_color_by_tex(r"f\,\Delta g", GREEN)
        eq1.set_color_by_tex(r"\Delta f\,g", RED)
        eq1.set_color_by_tex(r"\Delta f\,\Delta g", PURPLE)
        eq1.to_corner(UR).shift(DOWN * 1.0 + LEFT * 0.3)

        self.play(Write(eq1), run_time=1.5)
        self.wait(1)

        # ── 7. Divide by Δx ──────────────────────────────────────────────────
        eq2 = MathTex(
            r"\frac{\Delta A}{\Delta x}", "=",
            r"f\,\frac{\Delta g}{\Delta x}",
            "+",
            r"\frac{\Delta f}{\Delta x}\,g",
            "+",
            r"\frac{\Delta f}{\Delta x}\,\Delta g",
            font_size=28
        )
        eq2.next_to(eq1, DOWN, buff=0.55)

        self.play(TransformMatchingShapes(eq1.copy(), eq2), run_time=1.2)
        self.wait(0.8)

        # ── 8. Take the limit ─────────────────────────────────────────────────
        step3 = Text(r"As Δx → 0, the purple corner vanishes (it's second-order small).",
                     font_size=24, color=YELLOW).to_edge(UP)
        self.play(FadeOut(step2), FadeIn(step3))

        # Shrink the corner piece
        self.play(
            df_val.animate.set_value(0.05),
            dg_val.animate.set_value(0.05),
            run_time=1.5, rate_func=smooth
        )
        self.play(FadeOut(corner_rect), FadeOut(corner_lbl))
        self.wait(0.5)

        eq3 = MathTex(
            r"\frac{d}{dx}[fg]", "=",
            r"f\,\frac{dg}{dx}",
            "+",
            r"\frac{df}{dx}\,g",
            font_size=34, color=YELLOW
        )
        eq3.next_to(eq2, DOWN, buff=0.55)

        self.play(Write(eq3), run_time=1.3)
        self.wait(0.5)

        # ── 9. Final boxed result ─────────────────────────────────────────────
        self.play(FadeOut(step3))
        self.play(FadeOut(eq1), FadeOut(eq2))

        final = MathTex(
            r"(fg)' = f'g + fg'",
            font_size=52, color=YELLOW
        )
        box = SurroundingRectangle(final, color=YELLOW, buff=0.25, corner_radius=0.15)
        final_group = VGroup(final, box).to_corner(UR).shift(DOWN * 1.2 + LEFT * 0.3)

        self.play(Write(final), Create(box), run_time=1.2)

        proven = Text("Q.E.D.", font_size=30, color=GOLD).next_to(final_group, DOWN, buff=0.3)
        self.play(FadeIn(proven, scale=1.5))
        self.wait(2.5)

        # ── 10. Fade out everything ───────────────────────────────────────────
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1.2)
        self.wait(0.3)










