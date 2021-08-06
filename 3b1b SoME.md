## Titles
- Making Lenstra's algorithm with exceptions
- try/except blocks, but with algebraic number theory!
- The algorithm designed to fail

## Outline slide
1. Exceptions?!
2. Lenstra's algorithm
	1. Elliptic curves
	2. Groups
	3. Extended Euclidean algorithm

Try having some music in the background during these slides

## Script
> screen capture of programming a try-catch block 'Fireship' style

So in programming there's this concept of 'raising' or 'throwing' an exception. You may have heard of them in the context of try-catch blocks. The hardest thing about exceptions is that they can be raised by a function and handled by another function further up the call stack. Don't worry if you didn't understand that because we'll cover this idea by showing how it can be used to program my favorite algorithm in what might be its most intuitive form.

> manim animation of the factorization of 17776

We're going to look at a factoring algorithm. These are algorithms which take an integer and break it down into a series of numbers which, when multiplied together, give back the original integer.

> screen capture of certification details of wikipedia in browser (zoom into signature algorithm, public key, public key parameters)

'EC' here stands for elliptic curve. Cryptographers use them because they can be used to create secure systems using smaller keys. 

> manim animation of an elliptic curve, varying a parameter to decrease the size of the hole (with the formula shown: $y^2 = x^3 - x$ to $y^2 = x^3 - x + 1$)

They are these cool looking curves which can have a hole or a cusp. But the property that is most important for our algorithm of interest is the 'group structure' of these curves.

> manim animation of adding points on the curve

We say that a set has 'group structure' if we can define an operation on all the elements of that set that behaves similarly to addition. Say we have two points $P$ and $Q$ on an elliptic curve. Then to add $P$ and $Q$, we draw a line through them. The line will pass through the curve a third a time. Since the curve is symmetric, we can reflect the third point over the $x$-axis. We call this reflected point the sum of $P$ and $Q$. Why do we denote the point as 'negative' after reflection? Consider drawing a line through $P$ and $-P$. There is no third point. So we call the point 'at infinity' the identity element of addition on an elliptic curve. Just like zero with addition, we get the point at infinity when we add a point and its negation; we also a point back when we add the point at infinity, just like adding zero. 

> screen capture of code for addition

We can write code to do point additions on elliptic curves like this, but there is one more subtlety we need to consider before moving on to the algorithm. 

> manim animation converting the elliptic curve to one over a finite field (or more realistically for the algorithm, a composite number)

Let's see what happens when we look at them modulo a number, taking the remainder after diving by that number. We will journey to the land of modular arithmetic. 

> $\LaTeX$ representation of the point addition algorithm, with manim animating an emphasis box for each operation.

Addition. Subtraction. Multiplication. Division.

> manim animation for modular addition

Addition in modular arithmetic works more or less like a clock; hence, modular arithmetic is sometimes called clock arithmetic.

> manim animation for modular subtraction

Subtraction is just addition in the opposite direction.

> manim animation for modular multiplication (use the property $(a \cdot b) \mod n = (a \mod n)(b \mod n) \mod n$)

Modular multiplication behaves nicely due to this nice property.

> screen capture of using the python interactive prompt and doing calculations

But modular division is slightly more complicated. It requires finding a number called the modular multiplicative inverse. In regular arithmetic, if we wanted to divide by 5, we could just multiply by one fifth. Here in modular arithmetic land, we're going to use the extended Euclidean algorithm to find the modular multiplicative inverse. 

> 

---

> animation showing stack on right with code on left

So we see the exception is passed up -- raised -- through each function in the stack until it gets to a function that will handle the failure. It makes Lenstra's algorithm unique in that it's an algorithm built to fail. Thanks for watching.

> screen showing links in description to the code and the textbook