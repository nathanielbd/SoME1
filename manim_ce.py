from manim import *

"""
Base thumnail on this image: https://www.embedded.com/wp-content/uploads/media-1203925-maxim-ecdsa-figure-1-565.jpg
Throw `ThumbnailEC` and `ThumbnailFF` into Figma for final
"""

class ThumbnailEC(Scene):
	def construct(self):
		ax = Axes(
			x_range=[-1.3247, 2],
			y_range=[-1.3247, 2],
			# axis_config={'stroke_width': 10},
			tips=False
		)
		graph_top = ax.get_graph(
			lambda x: np.sqrt(x**3 - x + 1),
			# stroke_width=20,
			color=ORANGE
		)
		graph_bottom = ax.get_graph(
			lambda x: -np.sqrt(x**3 - x + 1),
			# stroke_width=20,
			color=ORANGE
		)
		line = ax.get_graph(
			lambda x: 1.1768178191460862263895685743891796710401469824300166243248806887
		)
		dot = Dot(ax.coords_to_point(-0.5773502691896257645091487805019574556476017512701268760186023264, 1.1768178191460862263895685743891796710401469824300166243248806887))
		label = MathTex('P').next_to(dot, UP)
		dot2 = Dot(ax.coords_to_point(1.1547, 1.17682))
		label2 = MathTex('Q').next_to(dot2, UP)
		# self.add(ax, graph_top, graph_bottom, dot, line, dot2)
		self.add(ax, graph_top, graph_bottom)
		self.play(
			GrowFromCenter(dot),
			GrowFromCenter(label)
		)
		self.play(Create(line))
		self.play(
			GrowFromCenter(dot2),
			GrowFromCenter(label2)
		)
		eq = MathTex('P + P = Q').shift(3*RIGHT+DOWN)
		self.play(
			Write(eq)
		)

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

class Fermat(Scene):
	def construct(self):
		wiles = ImageMobject('media/images/wiles.jpg').shift(3*LEFT)
		text = Text('Andrew Wiles \n (1953-Present)').shift(3*RIGHT)
		self.play(FadeIn(wiles))
		self.play(AddTextLetterByLetter(text))
		self.wait(2)

import random

class TitleCard(MovingCameraScene):
	def construct(self):
		ax = Axes(
			x_range=[-4, 4],
			y_range=[-4, 4],
			# axis_config={'stroke_width': 6},
			axis_config={'include_ticks': False},
			tips=False
		)
		ec = ImplicitFunction(
			lambda x, y: y**2 - x**3,
			x_max=4,
			x_min=-4,
			y_max=4,
			y_min=-4
		)
		self.play(
			Create(ax),
			Create(ec)
		)
		for i in range(3):
			A = random.randint(-3, 3)
			B = random.randint(-3, 3)
			new_ec = ImplicitFunction(
				lambda x, y: y**2 - x**3 - A*x - B,
				x_max=4,
				x_min=-4,
				y_max=4,
				y_min=-4
			)
			self.play(
				Transform(ec, new_ec)
			)
			self.wait(1)
		title = Text('The algorithm built to fail').scale(100)
		self.add(title)
		self.play(self.camera.frame.animate.scale(100))

class GroupTransition(ThreeDScene):
	def construct(self):
		q1 = Text('How will we use elliptic curves?')
		self.play(GrowFromCenter(q1))
		self.play(q1.animate.shift(UP))
		# q2 = MarkupText('What are elliptic curves?').next_to(q1, DOWN)
		q2_mu = MarkupText('What <i>are</i> elliptic curves?').next_to(q1, DOWN)
		# self.play(GrowFromCenter(q2))
		# self.play(TransformMatchingShapes(q2, q2_mu))
		self.play(GrowFromCenter(q2_mu))
		group = Text('Group Structure').set_color(GREEN).scale(0.01)\
			# .rotate_about_origin(PI)
		self.add(group)
		self.move_camera(theta=1.5*PI, added_anims=[group.animate.scale(100), Uncreate(q2_mu), Uncreate(q1)])
		self.wait(1)

class GroupRules(Scene):
	def construct(self):
		g = MathTex(r'\text{Group}: \{G, +\}')
		self.play(FadeIn(g))
		r1 = MathTex(r'\text{For all } a, b, c \text{ in } G \text{ such that }(a + b) + c = a + (b + c)')
		self.wait(1)
		self.play(
			g.animate.shift(UP),
			FadeIn(r1)
		)
		r2 = MathTex(r'\text{There exists } 0 \text{ in } G \text{ such that for all } a \text{ in } G, 0 + a = a = a + 0')
		self.wait(1)
		self.play(
			g.animate.shift(UP),
			r1.animate.shift(UP),
			FadeIn(r2)
		)
		r3 = MathTex(r'\text{For all } a \text{ in } G \text{ there exists } -a \text{ in } G \\ \text{ such that } a + -a = 0 = -a + a').shift(DOWN)
		self.wait(1)
		self.play(
			FadeIn(r3)
		)
		self.wait(1)

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
		r_label = MathTex('-P').next_to(r, RIGHT)
		# print(ec.get_anchors())
		rp = Dot([r.get_center()[0], -r.get_center()[1], 0])
		rp_label = MathTex("P").next_to(rp, RIGHT)
		line = Line(p.get_center(), q.get_center()).scale(5)
		line2 = Line(r.get_center(), rp.get_center()).scale(10)
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
		# self.play(
		# 	Wiggle(r),
		# 	Wiggle(r_label)
		# )
		# r_copy = r.copy()
		# self.add(r_copy)
		# self.play(
		# 	r_copy.animate.move_to(rp.get_center())
		# )
		# self.play(
		# 	GrowFromCenter(rp),
		# 	GrowFromCenter(rp_label)
		# )
		sum = MathTex(r'-P + P = \mathcal{O}').move_to([4, -1, 0])
		# self.play(Write(sum))
		# self.play(
		# 	Circumscribe(r_label)
		# )
		# self.play(
		# 	FadeOut(p),
		# 	FadeOut(p_label),
		# 	FadeOut(q),
		# 	FadeOut(q_label),
		# 	FadeOut(line)
		# )
		# self.play(
		# 	Create(line2)
		# )
		# self.play(Write(sum))
		# hmmm = Text('???').move_to(r.get_center()+UP*10)
		# self.add(hmmm)
		# self.play(
		# 	self.camera.frame.animate.shift(UP*10)
		# )
		# id = MathTex(r'\mathcal{O}').move_to(hmmm.get_center())
		# self.play(
		# 	Transform(hmmm, id)
		# )

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

class Identity2(Scene):
	def construct(self):
		x = MathTex('x').set_color(RED)
		x_sum = MathTex('x', '+0')
		x_sum[0].set_color(RED)
		x_copy = x.copy()
		p = MathTex('P').set_color(RED)
		p_sum = MathTex('P', r'+\mathcal{O}')
		p_sum[0].set_color(RED)
		p_copy = p.copy()
		self.add(x)
		self.play(Transform(x, x_sum))
		self.play(Transform(x, x_copy))
		self.play(
			x.animate.shift(UP),
			FadeIn(p)
		)
		self.play(Transform(p, p_sum))
		self.play(Transform(p, p_copy))

class AdditionAlgorithm(Scene):
	def construct(self):
		formula = MathTex('Y^2 = X^3 + ', 'A', 'X +', 'B').shift(UP*3)
		a = MathTex(r'\text{if }', 'P', r'=\mathcal{O}\text{, then }', 'P',  '+', 'Q', '=', 'Q').next_to(formula, DOWN)
		b = MathTex(r'\text{else if }', 'Q', r'=\mathcal{O}\text{, then }', 'P', '+', 'Q', '=', 'P').next_to(a, DOWN)
		c = MathTex(r'\text{else let }' , 'P', '=(', 'x_p', ',', 'y_p', r') \text{ and }', 'Q', '=(', 'x_q', ',', 'y_q', ')').next_to(b, DOWN)
		d = MathTex(r'\text{if }', 'x_p', '=', 'x_q', r'\text{ and }', 'y_p', '= -', 'y_q', r'\text{, then }', 'P', '+', 'Q', r'=\mathcal{O}').next_to(c, DOWN)
		e = MathTex(r'\text{else let } \lambda=\begin{cases}\frac{y_q-y_p}{x_q-x_p} & \text{if }P\not=Q\\ \frac{3x_p^2 +A}{2y_p} & \text{if }P=Q\end{cases}').next_to(d, DOWN)
		f = MathTex(r'\text{let }x_r = \lambda^2 - x_p - x_q\text{ and } y_r = \lambda(x_1-x_3)- y_1').next_to(e, DOWN)
		g = MathTex(r'\text{let }R = (x_r, y_r) \text{, then }P + Q = R').next_to(f, DOWN)
		self.play(FadeIn(formula))
		self.wait(1)
		self.play(
			FadeIn(a),
			FadeIn(b)
		)
		self.wait(1)
		self.play(FadeIn(c))
		self.wait(1)
		self.play(FadeIn(d))
		self.wait(1)
		self.play(FadeIn(e))
		self.wait(1)
		self.play(FocusOn(e))
		self.play(Indicate(formula))
		self.wait(1)
		self.play(FadeIn(f))
		self.wait(1)
		self.play(FadeIn(g))
		self.wait(1)

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
		# self.play(
		# 	Create(ec),
		# 	Write(formula)
		# )
		ec_copy = ec.copy()
		formula_copy = formula.copy()
		self.add(ec, formula)
		self.wait(2)
		self.play(
			Transform(ec, dots),
			Transform(formula, mod_formula)
		)
		self.wait(2)
		self.play(
			Transform(ec, ec_copy),
			Transform(formula, formula_copy)
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
		label = MathTex('1 + ', '0', r'\equiv 1 \mod 12').shift(2.5*UP)
		self.play(
			Create(circle),
			Create(line),
			Create(label)
		)
		for i in range(2, 16):
			self.play(
				line.animate.rotate_about_origin(-2*PI/12),
				Transform(label, MathTex(f'1 + {i-1} \\equiv {i % 12} \\mod 12').shift(2.5*UP))
			)

class ModSub(Scene):
	def construct(self):
		circle = Circle(radius=2)
		line = Line(ORIGIN, UP*2).rotate_about_origin(-2*PI/12*4)
		label = MathTex(r'4 - 0 \equiv 4 \mod 12').shift(2.5*UP)
		self.add(circle, line, label)
		for i in range(1, 17):
			self.play(
				line.animate.rotate_about_origin(2*PI/12),
				Transform(label, MathTex(f'4 - {i} \\equiv {(4-i) % 12} \\mod 12').shift(2.5*UP))
			)

class ModMul(Scene):
	def construct(self):
		prop = MathTex(r'(a \cdot b) \mod n', '\equiv', r'(a \mod n)', r'(b \mod n)', r'\mod n')
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
		final = MathTex(r'au \equiv 1 \mod b')
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

class Aha(Scene):
	def construct(self):
		what_if = MathTex(r'\text{What if }\gcd(a, N) \not= 1\text{?}')
		self.play(GrowFromCenter(what_if))

"""
Example 6.23 in book
"""

class Ex623(MovingCameraScene):
	def construct(self):
		self.camera.frame.save_state()
		ax = Axes(
			x_range=[-60, 187],
			y_range=[-60, 187],
			axis_config={'include_ticks': False},
			tips=False
		)
		diffs = np.array([[(y**2 - x**3 - 3*x - 7) % 187 for y in range(187)] for x in range(187)])
		pts = np.argwhere(diffs==0)
		dots = VGroup(*[Dot(point=ax.coords_to_point(pt[0], pt[1]), color=ORANGE) for pt in pts])
		self.add(ax, dots)
		p_label = MathTex('P').next_to(dots[30], DOWN)
		# 2P is 38
		# 3P is 46
		p2_label = MathTex('2P').next_to(dots[38], UP)
		p3_label = MathTex('3P').next_to(dots[46], RIGHT+DOWN)
		formula = MathTex(r'E: Y^2 = X^3 + 3X + 7 \mod 187').move_to([1, -2.5, 0])
		self.add(formula)
		self.play(
			Indicate(dots[30]),
			GrowFromCenter(p_label)
		)
		self.play(
			Indicate(dots[38]),
			GrowFromCenter(p2_label)
		)
		self.play(
			Indicate(dots[46]),
			GrowFromCenter(p3_label)
		)
		self.play(
			self.camera.frame.animate.shift(DOWN*6)
		)
		ps = MathTex(r'2P &= (', '43', r', 126) \\ 3P &= (', '54', ', 105)').next_to(formula, DOWN)
		p5 = MathTex('5P = 2P + 3P').next_to(ps, DOWN)
		slope = MathTex(r'\lambda=\begin{cases}\frac{y_3-y_2}{x_3-x_2} & \text{if }2P\not=3P\\ \frac{3x_2^2 +A}{2y_2} & \text{if }2P=3P\end{cases}').next_to(p5, DOWN)
		slope_case = MathTex(r'\lambda=', r'\frac{y_3-y_2}{x_3-x_2}').move_to(slope.get_center())
		slope_inv = MathTex(r'\lambda=y_3-y_2 \cdot', r'\frac{1}{x_3-x_2}').move_to(slope.get_center())
		slope_plug = MathTex(r'\lambda=y_3-y_2 \cdot \frac{1}{54 - 43} = y_3-y_2 \cdot \frac{1}{11} \mod 187').move_to(slope.get_center())
		euclid_out = MathTex(r'au + Nv = \gcd(a, N)').next_to(slope, DOWN)
		euclid_plug = MathTex(r'11u + 187v = \gcd(11, 187)').move_to(euclid_out.get_center())
		euclid_final = MathTex(r'11u + 187v = \gcd(11, 187) = 11').move_to(euclid_out.get_center())
		self.play(Write(ps))
		self.play(Write(p5))
		self.play(Write(slope))
		self.play(TransformMatchingShapes(slope, slope_case))
		self.play(Circumscribe(slope_case[1]))
		self.play(TransformMatchingShapes(slope_case, slope_inv))
		self.play(ShowPassingFlash(Underline(slope_inv[1])))
		self.play(
			TransformMatchingShapes(slope_inv, slope_plug),
			Indicate(ps[1]),
			Indicate(ps[3])
		)
		self.play(Write(euclid_out))
		self.play(TransformMatchingShapes(euclid_out, euclid_plug))
		self.play(Transform(euclid_plug, euclid_final))
		factors = MathTex(r'11 \cdot 17 = 187').next_to(euclid_out, DOWN)
		self.play(Write(factors))

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

class Lenstra(Scene):
	def construct(self):
		img1 = ImageMobject('media/images/Hendrik_Lenstra_MFO.jpg').scale(2)
		img2 = ImageMobject('media/images/lenstra.jfif').scale(2)
		img3 = ImageMobject('media/images/lenstra_award.jfif').scale(2)
		self.play(FadeIn(img1))
		self.wait(2)
		self.play(
			FadeOut(img1),
			FadeIn(img2)
		)
		self.wait(2)
		self.play(
			FadeOut(img2),
			FadeIn(img3)
		)

class EndQuote(Scene):
	def construct(self):
		# escher_blank = ImageMobject('media/images/escher_blank.jpg').scale(600/930).shift(LEFT*4)
		# escher_filled = ImageMobject('media/images/escher_filled.jfif').scale(600/390).shift(LEFT*4)
		# self.play(FadeIn(escher_blank))
		lenstra = ImageMobject('media/images/lenstra_award.jfif').scale(2).shift(LEFT*4)
		self.add(lenstra)
		quote = Text(
			"The main application of \n"
			"Pure Mathematics is to \n"
			"make you happy \n"
			"		---Hendrik Lenstra"
		).shift(RIGHT*3)
		self.add(quote)
		# self.play(AddTextLetterByLetter(quote))
		# self.play(
		# 	FadeOut(escher_blank),
		# 	FadeIn(escher_filled)
		# )
