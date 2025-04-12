from manim import *
import math # Import math for PI / degrees

# Use `manim -pql scene.py EuclidVCorrected` to render
# or `manim -pqm scene.py EuclidVCorrected` for medium quality
# or `manim -pqh scene.py EuclidVCorrected` for high quality

class EuclidVCorrected(Scene):
    def construct(self):
        # 1. Title
        title = Title("Euclid's Fifth Postulate (Parallel Postulate)")
        self.play(Write(title))
        self.wait(1)

        # 2. Define Lines and Intersection Points
        # Transversal Line T (more vertical)
        T = Line(UP * 3 + LEFT * 0.5, DOWN * 3 + RIGHT * 0.5, color=BLUE)

        # Line L1 (slanted slightly downwards to the right)
        L1_start_point = LEFT * 4 + UP * 1.5
        L1_end_point = RIGHT * 1 + UP * 1.0 # Initial short segment
        L1 = Line(L1_start_point, L1_end_point, color=YELLOW)

        # Line L2 (slanted slightly upwards to the right)
        L2_start_point = LEFT * 4 + DOWN * 1.5
        L2_end_point = RIGHT * 1 + DOWN * 1.0 # Initial short segment
        L2 = Line(L2_start_point, L2_end_point, color=GREEN)

        # Calculate intersection points (still useful for placing dots and labels)
        P1 = line_intersection(T.get_start_and_end(), L1.get_start_and_end())
        P2 = line_intersection(T.get_start_and_end(), L2.get_start_and_end())

        # Create Dot markers for intersection points
        dot_P1 = Dot(P1, color=RED)
        dot_P2 = Dot(P2, color=RED)

        # 3. Draw Initial Setup
        self.play(Create(T), Create(L1), Create(L2))
        self.play(FadeIn(dot_P1), FadeIn(dot_P2))
        self.wait(1)

        # 4. Define and Show Interior Angles on the "less than 180" side (right side)
        # Angle determines vertex from line intersection implicitly
        # Adjust quadrant/other_angle as needed for visualization

        # Angle alpha (at P1, between T downwards and L1 rightwards)
        # We want the angle on the bottom-right relative to the intersection P1
        angle_alpha = Angle(T, L1, radius=0.6, quadrant=(1,-1), other_angle=False, color=ORANGE)
        alpha_label = MathTex(r"\alpha", color=ORANGE).move_to(
            Angle(T, L1, radius=0.6 + 3*SMALL_BUFF, quadrant=(1,-1), other_angle=False).point_from_proportion(0.5)
        )


        # Angle beta (at P2, between T upwards and L2 rightwards)
        # We want the angle on the top-right relative to the intersection P2
        angle_beta = Angle(L2, T, radius=0.6, quadrant=(1,1), other_angle=False, color=PURPLE)
        beta_label = MathTex(r"\beta", color=PURPLE).move_to(
             Angle(L2, T, radius=0.6 + 3*SMALL_BUFF, quadrant=(1,1), other_angle=False).point_from_proportion(0.5)
        )

        # Check: Visually, alpha + beta on the right side should be < 180 degrees
        self.play(Create(angle_alpha), Write(alpha_label))
        self.play(Create(angle_beta), Write(beta_label))
        self.wait(1)

        # 5. State the Condition
        # Calculate actual angles for display (optional, but good for verification)
        # Note: Manim angles are in radians
        alpha_val_rad = angle_alpha.get_value()
        beta_val_rad = angle_beta.get_value()
        sum_deg = math.degrees(alpha_val_rad + beta_val_rad)

        # Display the condition text
        # condition_text = MathTex(r"\alpha + \beta < 180^\circ", color=WHITE).to_corner(UL)
        condition_text = MathTex(
            r"\alpha + \beta", f" = {sum_deg:.1f}^\circ < 180^\circ", color=WHITE
            ).to_corner(UL)
        condition_text.set_color_by_tex(r"\alpha", ORANGE)
        condition_text.set_color_by_tex(r"\beta", PURPLE)

        self.play(Write(condition_text))
        self.wait(1.5)

        # 6. Extend the Lines on the side where angles < 180° (right side)
        # Calculate the actual intersection of the extended lines
        intersect_point = line_intersection(
            (L1.get_start(), L1.get_end()), # Use original segment ends to define infinite line direction
            (L2.get_start(), L2.get_end())
        )

        # Ensure intersection is sufficiently far right for dramatic effect
        # If lines are nearly parallel, intersection might be very far
        # We can manually set a far point if needed, but let's try calculated first
        # Add a small vector in the line's direction to extend slightly past intersection
        extension_buffer = 0.5

        intersect_dot = Dot(intersect_point, color=RED, radius=0.1)
        intersect_label = Text("Intersection", font_size=24).next_to(intersect_dot, UP, buff=0.2)

        # Animate the extension using put_start_and_end_on
        self.play(
            L1.animate.put_start_and_end_on(L1.get_start(), intersect_point + L1.get_unit_vector() * extension_buffer),
            L2.animate.put_start_and_end_on(L2.get_start(), intersect_point + L2.get_unit_vector() * extension_buffer),
            run_time=3,
            rate_func=linear
        )
        self.play(FadeIn(intersect_dot, scale=0.5), Write(intersect_label))
        self.wait(2)

        # 7. Display Postulate Text
        postulate_text_lines = [
            "If a straight line falling on two straight lines",
            "makes the interior angles on the same side",
            "less than two right angles (180°),",
            "the two straight lines, if extended indefinitely,",
            "meet on that side on which the angles are",
            "less than two right angles."
        ]
        postulate_vg = VGroup(*[Text(line, font_size=28) for line in postulate_text_lines])
        postulate_vg.arrange(DOWN, center=False, aligned_edge=LEFT)
        postulate_vg.to_corner(DR) # Position text at the bottom right

        # Fade out elements that might clutter the text area
        self.play(
            FadeOut(condition_text),
            FadeOut(alpha_label),
            FadeOut(beta_label),
            FadeOut(intersect_label) # Keep dots and lines for context
         )

        self.play(Write(postulate_vg))
        self.wait(5) # Hold the final scene