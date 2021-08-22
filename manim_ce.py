from manim import *

"""
Base thumnail on this image: https://www.embedded.com/wp-content/uploads/media-1203925-maxim-ecdsa-figure-1-565.jpg
Throw `ThumbnailEC` and `ThumbnailFF` into Figma for final
"""

class ThumbnailEC(Scene):
	def construct(self):
		ax = Axes(
			x_range=[-3, 6],
			y_range=[-15, 15],
			axis_config={'stroke_width': 10},
			tips=False
		)
		graph_top = ax.get_graph(
			lambda x: np.sqrt(x**3 - 3*x + 18),
			stroke_width=20,
			color=ORANGE
		)
		graph_bottom = ax.get_graph(
			lambda x: -np.sqrt(x**3 - 3*x + 18),
			stroke_width=20,
			color=ORANGE
		)
		self.add(ax, graph_top, graph_bottom)

class ThumbnailFF(Scene):
	def construct(self):
		ax = Axes(
			x_range=[0, 22],
			y_range=[0, 22],
			axis_config={'stroke_width': 6},
			tips=False
		)
		diffs = np.array([[(y**2 - x**3 - 13*x - 7) % 23 for y in range(23)] for x in range(23)])
		pts = np.argwhere(diffs==0)
		dots = VGroup(*[Dot(point=ax.coords_to_point(pt[0], pt[1]), color=ORANGE, radius=0.15) for pt in pts])
		self.add(ax, dots)

"""
Reference to Jon Bois's 17776
"""

class FactorBois(Scene):
	def construct(self):
		n = MathTex('17776')
		n2 = n.copy()
		n3 = n.copy().shift(UP)
		s1 = MathTex(r'2 \cdot 8888')
		s2 = MathTex(r'2 \cdot 2 \cdot 4444')
		s3 = MathTex(r'2 \cdot 2 \cdot 2 \cdot 2222')
		s4 = MathTex(r'2 \cdot 2 \cdot 2 \cdot 2 \cdot 1111')
		s5 = MathTex(r'2 \cdot 2 \cdot 2 \cdot 2 \cdot 11 \cdot 101')
		s6 = MathTex(r'4 \cdot 2 \cdot 2 \cdot 11 \cdot 101')
		s7 = MathTex(r'8 \cdot 2 \cdot 11 \cdot 101')
		s8 = MathTex(r'16 \cdot 11 \cdot 101')
		s9 = MathTex(r'176 \cdot 101')
		self.add(n)
		self.play(Transform(n2, n3))
		out_steps = [s1, s2, s3, s4, s5]
		for step in out_steps:
			self.play(Transform(n, step), run_time=0.5)
		ul = Underline(n, color=YELLOW)
		self.play(Create(ul))
		self.wait(2)
		self.play(FadeOut(ul))
		in_steps = [s6, s7, s8, s9]
		for step in in_steps:
			self.play(Transform(n, step), run_time=0.5)
		self.play(Transform(n, MathTex('17776')))
		self.play(Transform(n2, MathTex('17776')), n.animate.set_color(GREEN))

# implicit algebraic curves are not yet supported by ManimCE
from implicit import ImplicitFunction

class CuspNoCusp(Scene):
	def construct(self):
		ec = ImplicitFunction(
			lambda x, y: y**2 - x**3 + x,
			x_max = 4,
			x_min = -4,
			y_max = 4,
			y_min = -4
		).set_color(ORANGE)
		ax = Axes(
			x_range=[-4, 4],
			y_range=[-4, 4],
			axis_config={'include_ticks': False},
			tips=False
		)
		line = Line([-5, -2, 0], [-1, -2, 0])
		dot = Dot([-5, -2, 0]).set_color(BLUE)
		label = MathTex('a').set_color(BLUE).next_to(dot, UP)
		progress = VMobject()
		progress.set_points_as_corners([dot.get_center(), dot.get_center()]).set_color(BLUE)
		formula = MathTex('y^2 = x^3 - x + ', 'a').move_to([-3, 2, 0])
		formula[1].set_color(BLUE)
		def update_ec(prev_ec):
			new_ec = ImplicitFunction(
				lambda x, y: y**2 - x**3 + x - (dot.get_center()[0] + 5)/4,
				x_max = 4,
				x_min = -4,
				y_max = 4,
				y_min = -4
			).set_color(ORANGE)
			prev_ec.become(new_ec)
		def update_progress(prev_progress):
			new_progress = prev_progress.copy().set_points_as_corners([[-5, -2, 0], dot.get_center()])
			prev_progress.become(new_progress)
		def update_label(prev_label):
			new_label = prev_label.copy().next_to(dot, UP)
			prev_label.become(new_label)
		ec.add_updater(update_ec)
		progress.add_updater(update_progress)
		label.add_updater(update_label)
		left = MathTex('0').next_to([-5, -2, 0], DOWN)
		right = MathTex('1').next_to([-1, -2, 0], DOWN)
		self.add(ec, ax, line, dot, formula, label, progress, left, right)
		self.play(dot.animate.shift(RIGHT*4))
		self.play(dot.animate.shift(LEFT*4))

class PointAddition(MovingCameraScene):
	def construct(self):
		self.camera.frame.save_state()
		ec = ImplicitFunction(
			lambda x, y: y**2 - x**3 + 3*x - 3,
			x_max = 6,
			x_min = -6,
			y_max = 6,
			y_min = -6
		).set_color(ORANGE)
		ax = Axes(
			x_range=[-6, 6],
			y_range=[-6, 6],
			axis_config={'include_ticks': False},
			tips=False
		)
		p = Dot(ec.get_anchors()[95])
		p_label = MathTex('P').next_to(p, DOWN+RIGHT)
		q = Dot(ec.get_anchors()[145])
		q_label = MathTex('Q').next_to(q, DOWN)
		r = Dot(ec.get_anchors()[174])
		r_label = MathTex('-R').next_to(r, DOWN+RIGHT)
		# print(ec.get_anchors())
		rp = Dot([r.get_center()[0], -r.get_center()[1], 0])
		rp_label = MathTex("R").next_to(rp, RIGHT)
		line = Line(p.get_center(), q.get_center()).scale(5)
		line2 = Line(r.get_center(), rp.get_center()).scale(5)
		# self.add(ec, ax, p, q, r, line, rp, p_label, q_label, r_label, rp_label)
		self.add(ax)
		self.play(Create(ec))
		self.play(
			FadeIn(p),
			FadeIn(p_label)
		)
		self.play(
			FadeIn(q),
			FadeIn(q_label)
		)
		self.play(Create(line))
		self.play(
			GrowFromCenter(r),
			GrowFromCenter(r_label)
		)
		self.play(
			Wiggle(r),
			Wiggle(r_label)
		)
		r_copy = r.copy()
		self.add(r_copy)
		self.play(
			r_copy.animate.move_to(rp.get_center())
		)
		self.play(
			GrowFromCenter(rp_label)
		)
		sum = MathTex('P + Q = R').move_to([-3, 3, 0])
		self.play(Write(sum))
		self.play(
			Circumscribe(r_label)
		)
		self.play(
			FadeOut(p),
			FadeOut(p_label),
			FadeOut(q),
			FadeOut(q_label),
			FadeOut(line)
		)
		self.play(
			Create(line2)
		)
		hmmm = Text('???').move_to(r.get_center()+UP*10)
		self.add(hmmm)
		self.play(
			self.camera.frame.animate.shift(UP*10)
		)
		id = MathTex(r'\mathcal{O}').move_to(hmmm.get_center())
		self.play(
			Transform(hmmm, id)
		)