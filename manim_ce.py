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

