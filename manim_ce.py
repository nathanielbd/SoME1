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

class Identity(Scene):
	def construct(self):
		x = MathTex('x').set_color(RED)
		x_sum = MathTex('x', '-x')
		x_sum[0].set_color(RED)
		x_sum[1].set_color(BLUE)
		zero = MathTex('0')
		p = MathTex('P').set_color(RED)
		p_sum = MathTex('P', '-P')
		p_sum[0].set_color(RED)
		p_sum[1].set_color(BLUE)
		id = MathTex(r'\mathcal{O}')
		self.add(x)
		self.play(Transform(x, x_sum))
		self.play(Transform(x, zero))
		self.play(FadeOut(x))
		self.play(FadeIn(p))
		self.play(Transform(p, p_sum))
		self.play(Transform(p, id))

class AdditionAlgorithm(Scene):
	def construct(self):
		formula = MathTex('Y^2 = X^3 + ', 'A', 'X +', 'B').shift(UP*3)
		# vroom
		# formula[1].set_color(YELLOW)
		# formula[3].set_color(ORANGE)
		a = MathTex(r'\text{if }', 'P', r'=\mathcal{O}\text{, then }', 'P',  '+', 'Q', '=', 'Q').next_to(formula, DOWN)
		# a[1].set_color(PURPLE)
		# a[3].set_color(PURPLE)
		# a[5].set_color(GREEN)
		# a[7].set_color(GREEN)
		b = MathTex(r'\text{else if }', 'Q', r'=\mathcal{O}\text{, then }', 'P', '+', 'Q', '=', 'P').next_to(a, DOWN)
		# b[1].set_color(GREEN)
		# b[3].set_color(PURPLE)
		# b[5].set_color(GREEN)
		# b[7].set_color(PURPLE)
		c = MathTex(r'\text{else let }' , 'P', '=(', 'x_p', ',', 'y_p', r') \text{ and }', 'Q', '=(', 'x_q', ',', 'y_q', ')').next_to(b, DOWN)
		# c[1].set_color(PURPLE)
		# c[3].set_color(PURPLE)
		# c[5].set_color(PURPLE)
		# c[7].set_color(GREEN)
		# c[9].set_color(GREEN)
		# c[11].set_color(GREEN)
		# self.add(formula, a, b, c)
		d = MathTex(r'\text{if }', 'x_p', '=', 'x_q', r'\text{ and }', 'y_p', '= -', 'y_q', r'\text{, then }', 'P', '+', 'Q', r'=\mathcal{O}').next_to(c, DOWN)
		# d[1].set_color(PURPLE)
		# d[3].set_color(GREEN)
		# d[5].set_color(PURPLE)
		# d[7].set_color(GREEN)
		# d[9].set_color(PURPLE)
		# d[11].set_color(GREEN)
		# self.add(d)
		e = MathTex(r'\text{else let } \lambda=\begin{cases}\frac{y_q-y_p}{x_q-x_p} & \text{if }P\not=Q\\ \frac{3x_p^2 +A}{2y_p} & \text{if }P=Q\end{cases}').next_to(d, DOWN)
		# e = MathTex(r'\text{else let } \lambda=\begin{cases}\frac{', 'y_q', '-',  'y_p', '}{', 'x_q', '-', 'x_p', r'} & \text{if }', 'P', \
		# 	r'\not=', 'Q', r'\\ \frac{3', 'x_p', '^2 +', 'A', '}{2', 'y_p', r'} & \text{if }', 'P', '=', 'Q', r'\end{cases}')
		# e[1].set_color(GREEN)
		# e[3].set_color(PURPLE)
		# e[5].set_color(GREEN)
		# e[7].set_color(GREEN)
		# e[9].set_color(PURPLE)
		# e[11].set_color(PURPLE)
		# e[13].set_color(GREEN)
		# e[15].set_color(PURPLE)
		# e[17].set_color(YELLOW)
		# e[19].set_color(PURPLE)
		# e[21].set_color(PURPLE)
		# e[23].set_color(GREEN)
		# self.add(e)
		f = MathTex(r'\text{let }x_r = \lambda^2 - x_p - x_q\text{ and } y_r = \lambda(x_1-x_3)- y_1').next_to(e, DOWN)
		g = MathTex(r'\text{let }R = (x_r, y_r){, then }P + Q = R').next_to(f, DOWN)
		self.play(FadeIn(formula))
		self.play(
			FadeIn(a),
			FadeIn(b)
		)
		self.play(FadeIn(c))
		self.play(FadeIn(d))
		self.play(FadeIn(e))
		self.play(FocusOn(e))
		self.play(Indicate(formula))
		self.play(FadeIn(f))
		self.play(FadeIn(g))

class ECtoFF(Scene):
	def construct(self):
		formula = MathTex('E: Y^2 = X^3 + AX + B').move_to([-3, 2, 0])
		ec = ImplicitFunction(
			lambda x, y: y**2 - x**3 + 3*x - 18,
			x_max=12,
			x_min=-6,
			y_max=30,
			y_min=-30
		).set_color(ORANGE).scale(0.5)
		ax = Axes(
			x_range=[0, 22],
			y_range=[0, 22],
			axis_config={'stroke_width': 6},
			tips=False
		)
		diffs = np.array([[(y**2 - x**3 - 13*x - 7) % 23 for y in range(23)] for x in range(23)])
		pts = np.argwhere(diffs==0)
		dots = VGroup(*[Dot(point=ax.coords_to_point(pt[0], pt[1]), color=ORANGE, radius=0.15) for pt in pts])
		mod_formula = MathTex(r'E: Y^2 = X^3 + AX + B \mod N')
		self.play(
			Create(ec),
			Write(formula)
		)
		self.play(
			Transform(ec, dots),
			Transform(formula, mod_formula)
		)

class AAOps(Scene):
	def construct(self):
		e = MathTex(r'\lambda=\begin{cases}\frac{y_q-y_p}{x_q-x_p} & \text{if }P\not=Q\\ \frac{3x_p^2 +A}{2y_p} & \text{if }P=Q\end{cases}')
		self.play(
			FadeIn(e)
		)
		add = ORIGIN+0.35*LEFT+0.1*DOWN
		sub = ORIGIN+0.55*LEFT+0.75*UP
		mul = ORIGIN+LEFT+0.1*DOWN
		div = Line(ORIGIN+1.15*LEFT+0.375*DOWN, ORIGIN+0.375*DOWN+0.1*RIGHT, stroke_opacity=0)
		self.play(Flash(add))
		self.play(Flash(sub))
		self.play(Flash(mul))
		self.play(Circumscribe(div))

class ModAdd(Scene):
	def construct(self):
		circle = Circle(radius=2)
		line = Line(ORIGIN, UP*2).rotate_about_origin(-2*PI/12)
		label = MathTex('1 + ', '0', r'\mod 12 =', '1').shift(2.5*UP)
		self.play(
			Create(circle),
			Create(line),
			Create(label)
		)
		for i in range(2, 16):
			self.play(
				line.animate.rotate_about_origin(-2*PI/12),
				Transform(label, MathTex(f'1 + {i-1} \\mod 12 = {i % 12}').shift(2.5*UP))
			)

class ModSub(Scene):
	def construct(self):
		circle = Circle(radius=2)
		line = Line(ORIGIN, UP*2).rotate_about_origin(-2*PI/12*4)
		label = MathTex(r'4 - 0 \mod 12 = 4').shift(2.5*UP)
		self.add(circle, line, label)
		for i in range(1, 6):
			self.play(
				line.animate.rotate_about_origin(2*PI/12),
				Transform(label, MathTex(f'4 - {i} \\mod 12 = {(4 - i) % 12}').shift(2.5*UP))
			)

class ModMul(Scene):
	def construct(self):
		prop = MathTex(r'(a \cdot b) \mod n', '=', r'(a \mod n)', r'(b \mod n)', r'\mod n')
		self.play(Write(prop))
		self.play(ShowPassingFlash(Underline(prop[0])))
		self.play(ShowPassingFlash(Underline(prop[2])))
		self.play(ShowPassingFlash(Underline(prop[3])))

class GCDEx(MovingCameraScene):
	def construct(self):
		ex1 = MathTex(r'\gcd(12, 18) = 6')
		re1 = MathTex(r'12 = 2 \cdot 6 \text{ and }18 = 3 \cdot 6', substrings_to_isolate='6').next_to(ex1, DOWN)
		re1.set_color_by_tex('6', YELLOW)
		ex2 = MathTex(r'\gcd(15, 16) = 1')
		re2 = MathTex(r'15 = 3 \cdot 5 \text{ and } 16 = 2 \cdot 2 \cdot 2 \cdot 2').next_to(ex2, DOWN)
		self.play(
			Write(ex1)
		)
		self.play(
			FadeIn(re1)
		)
		self.play(
			FadeOut(ex1),
			FadeOut(re1),
			FadeIn(ex2)
		)
		self.play(
			FadeIn(re2)
		)
		cross = Cross(re2)
		self.play(
			Create(cross)
		)
		self.play(
			Uncreate(cross),
			Uncreate(re2)
		)
		euclid_out = MathTex(r'au + bv = \gcd(a, b)')
		func = MathTex(r'a, b \rightarrow \textrm{EuclideanAlgorithm} \rightarrow u, b').next_to(euclid_out, DOWN)
		self.play(
			Transform(ex2, euclid_out)
		)
		self.play(
			FadeIn(func)
		)
		self.play(FadeOut(func))
		gcd_one = MathTex(r'au + bv = 1 \mod b')
		intermediate = MathTex(r'au - 1 = -bv \mod b')
		final = MathTex(r'au = 1 \mod b')
		self.play(
			Transform(ex2, gcd_one)
		)
		self.play(
			TransformMatchingShapes(ex2, intermediate)
		)
		self.play(
			TransformMatchingShapes(intermediate, final)
		)
		# add birds eye view of topics next
		# mul_inv = Text('Multiplicative Inverse').

import random

class RandomECs(Scene):
	def construct(self):
		ax = Axes(
			x_range=[-7, 22],
			y_range=[-7, 22],
			# axis_config={'stroke_width': 6},
			axis_config={'include_ticks': False},
			tips=False
		)
		diffs = np.array([[(y**2 - x**3) % 23 for y in range(23)] for x in range(23)])
		pts = np.argwhere(diffs==0)
		dots = VGroup(*[Dot(point=ax.coords_to_point(pt[0], pt[1]), color=ORANGE, radius=0.15) for pt in pts])
		A_line = Line([-6, 2, 0], [-4, 2, 0])
		a_line = Line([-6, 1, 0], [-4, 1, 0])
		b_line = Line([-6, 0, 0], [-4, 0, 0])
		A_dial = Dot([-6, 2, 0]).set_color(BLUE)
		A_belt = VMobject()
		A_belt.set_points_as_corners([A_dial.get_center(), A_dial.get_center()]).set_color(BLUE)
		def update_A_belt(prev_belt):
			new_belt = prev_belt.copy().set_points_as_corners([[-6, 2, 0], A_dial.get_center()])
			prev_belt.become(new_belt)
		A_belt.add_updater(update_A_belt)
		a_dial = Dot([-6, 1, 0]).set_color(GREEN)
		a_belt = VMobject()
		a_belt.set_points_as_corners([a_dial.get_center(), a_dial.get_center()]).set_color(GREEN)
		def update_a_belt(prev_belt):
			new_belt = prev_belt.copy().set_points_as_corners([[-6, 1, 0], a_dial.get_center()])
		a_belt.add_updater(update_a_belt)
		b_dial = Dot([-6, 0, 0]).set_color(PURPLE)
		b_belt = VMobject()
		b_belt.set_points_as_corners([b_dial.get_center(), b_dial.get_center()]).set_color(PURPLE)
		def update_b_belt(prev_belt):
			new_belt = prev_belt.copy().set_points_as_corners([[-6, 0, 0], b_dial.get_center()])
		b_belt.add_updater(update_b_belt)
		left = MathTex('0').next_to([-6, 0, 0], DOWN)
		right = MathTex('N').next_to([-4, 0, 0], DOWN)
		formula = MathTex('E: Y^2 = X^3 + ', 'A', r'X + B \\ B = ', 'b', '^2 - ', 'a', '^3 - ', 'A', 'a', r'\mod N, N = 23').move_to([1, -2.5, 0])
		# vroom
		formula[1].set_color(BLUE)
		formula[3].set_color(PURPLE)
		formula[5].set_color(GREEN)
		formula[7].set_color(BLUE)
		formula[8].set_color(GREEN)
		# formula.set_color_by_tex('A', BLUE)
		# formula.set_color_by_tex('a', GREEN)
		# formula.set_color_by_tex('b', PURPLE)
		N = 23
		self.add(ax, A_line, a_line, b_line, formula, left, right, dots)
		for i in range(3):
			A = random.randint(0, N)
			a = random.randint(0, N)
			b = random.randint(0, N)
			B = (b**2 - a**3 - A*a) % N
			new_diffs = np.array([[(y**2 - x**3 - A*x - B) % N for y in range(23)] for x in range(23)])
			new_pts = np.argwhere(new_diffs == 0)
			new_dots = VGroup(*[Dot(point=ax.coords_to_point(pt[0], pt[1]), color=ORANGE, radius=0.15) for pt in new_pts])
			self.play(
				A_dial.animate.move_to([-6, 2, 0] + A/(N-1)*2*RIGHT),
				a_dial.animate.move_to([-6, 1, 0] + a/(N-1)*2*RIGHT),
				b_dial.animate.move_to([-6, 0, 0] + b/(N-1)*2*RIGHT),
				Transform(dots, new_dots)
			)