## Titles
- Making Lenstra's algorithm with exceptions
- try/except blocks, but with algebraic number theory!
- The algorithm designed to fail

Choice: The algorithm designed to fail

Click-baity, but it's a good hint for the challenge in the script. Thumbnail can be an elliptic curve on the left, a right-facing arrow, and an elliptic curve in a finite field on the right in manim. Maybe add a confused pi creature and a '?!' in there at the bottom.

## Outline slide
1. Exceptions?!
2. Lenstra's algorithm
	1. Elliptic curves
	2. Groups
	3. Extended Euclidean algorithm

Try having some music in the background during these slides

Also perhaps draw an arrow with a label with each transition.

- Exceptions?! --> motivates learning --> Lenstra's algorithm
- Lenstra's algorithm --> requires learning --> Elliptic curves
- Elliptic curves --> have the properties of --> Groups
- Groups --> EC group operations are computed with --> Extended Euclidean algorithm

## Script
> screen capture of programming a try-catch block 'Fireship' style

So in programming there's this concept of 'raising' or 'throwing' an exception. You may have heard of them in the context of try-catch blocks. The hardest thing about exceptions is that they can be raised by a function and handled by another function further up the call stack. Don't worry if you didn't understand that because we'll cover this idea by showing how it can be used to program my favorite algorithm in its most intuitive form.

> manim animation of the factorization of 17776

We're going to look at a factoring algorithm. These are algorithms which take an integer and break it down into a series of numbers which, when multiplied together, give back the original integer.

> screen capture of certification details of wikipedia in browser (zoom into signature algorithm, public key, public key parameters)

'EC' here stands for elliptic curve. Cryptographers use them because they can be used to create secure systems using smaller keys. 

> manim animation of an elliptic curve, varying a parameter to decrease the size of the hole (with the formula shown: $y^2 = x^3 - x$ to $y^2 = x^3 - x + 1$)

They are these cool looking curves which can have a hole or a cusp. But the property that is most important for our algorithm of interest is the 'group structure' of these curves.


	If time, add a sentence to say that they were used in the famous proof of Fermat's last theorem. If not, add a footnote in the video


> manim animation of adding points on the curve

Roughly speaking, we say that a set has 'group structure' if we can define an operation on all the elements of that set that behaves similarly to addition. Say we have two points $P$ and $Q$ on an elliptic curve. Then to add $P$ and $Q$, we draw a line through them. The line will pass through the curve a third a time. Since the curve is symmetric, we can reflect the third point over the $x$-axis. We call this reflected point the sum of $P$ and $Q$. Why do we denote the point as 'negative' after reflection? Consider drawing a line through $P$ and $-P$. There is no third point. So we call the point 'at infinity' the identity element of addition on an elliptic curve. Just like zero with addition, we get the point at infinity when we add a point and its negation; we also a point back when we add the point at infinity, just like adding zero. 

> screen capture of pseudo code for addition

		(Try instead: We can compute point additions like this. Notice that it involves calculating the slope, $\\lambda$, which is just a rearrangement of point-slope form usually, but includes a special case when we are adding a point to itself, in which case we find the slope of the tangent line.)

We can write code to do point additions on elliptic curves like this, where $\lambda$ is result of computing the slope of the line between the points we are adding. But there is one more subtlety we need to consider before moving on to the algorithm. 

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

> manim animation of the GCD examples

The greatest common divisor, or $\gcd$, is the largest number that divides the both numbers of interest evenly. For example, the GCD of 12 and 18 is 6. On the other hand, the GCD of 16 and 15 is 1, since they share no factors. 

> animate everything fading but GCD and zoom out to reveal extended Euclidean algorithm equation: $au + bv = \gcd(a,b)$

This is the output of the extended Euclidean algorithm. Given $a$ and $b$, the algorithm will spit out the values of $u$ and $v$. It's a pretty simple algorithm, but for now let's focus on finding a modular multiplicative inverse. 

> animation of both modular multiplicative inverse and regular multiplicative inverse

Just like in regular arithmetic, we want the product of a number and its multiplicative inverse to be 1.

> substitute $\gcd(a,b)$ with 1

This means that a necessary condition for the existence of a modular multiplicative inverse is having a GCD equal to 1. With regular arithmetic, the only number without a multiplicative inverse is 0; we will see that having a GCD that is not 1 is like dividing by 0.

> rearranging of the equation to $au - 1 = -mv \mod m$

We can rearrange...

> rearranging of the equation to $au = 1 \mod m$

And of course, $-mv$ doesn't have any remainders when dividing by $m$. So $u$ is the modular multiplicative inverse of $a$!

> screen with all of the topics so far with a countdown in the bottom left

At this point I want to stop for a moment. Here's a challenge for you-- can you come up with a factoring algorithm from everything we've talked about so far? 

> animate arrows labeled with '?' between pairs of the topics

		Do I have enough time and space to label the arrows and/or review the relationships between the topics?

Try to think about the context in which every topic was introduced... and consider the title of this video your final hint. Pause the video and see if you can put it all together.

> countdown drops from 5, animate $\gcd \not= 1$

Alright, the secret is to consider the case where we don't get a GCD equal to 1. That means that there is a common divisor and so we have factored the number!

> animate example 6.23, with $\lambda$ formula on left and the elliptic curve and its finite field points overlaid on the right, with point coordinates below it (fade and highlight the elliptic curve when calculating slopes, etc.)

But how would that ever happen? Well, let's say we are trying to add these two points on the curve together. Using the slope formula, we need to do modular division, which means we need to find the modular multiplicative inverse of ... 11. This requires the computation of the GCD of 11 and 187, which is 11. So the slope is undefined, as if we divided by zero, and we fail to get a point from addition that isn't the one at infinity, but we find a factor of 187 to be 11!

> animate dials controlling $A$, $a$, $b$ parameters of the curve and set them haphazardly

Our algorithm will leverage this idea, taking random elliptic curves...

> animate computing $nP$ repeatedly, add a footnote clarifying that we compute multiples of the point using the fast *double-and-add* algorithm

And adding a point to itself repeatedly, in this case computing multiples of a random point by doubling it and adding it to itself, until we run into a point addition that makes us run into a GCD not equal to 1.

> Fireship-esque screen capture of code

When writing the algorithm in code, we need something to implement the idea of 'try doing stuff and if something goes wrong, handle it appropriately.' That 'something' is the concept of exceptions.

> the screen capture goes through the same example 6.23, but with the debugger and a stack visualization, highlighting parts of the code as I speak them out, moving to the stack visualization, then fading

Using python, we can start with creating a random point on a random elliptic curve. Then we can call our *double-and-add* point function in a loop, first wrapping it in a try block. The double-and-add function calls the point addition function. And the point addition function calls the extended Euclidean algorithm function when we need to find a modular multiplicative inverse to compute the slope. 

> zoom to stack visualization

Phew! At this point a lot of functions have been called and the computer keeps track of their order on the stack, with the earliest-called functions on the bottom, and the latest-called functions at the top.

> zoom back out

At this point, the computer can go through the motions of the extended Euclidean algorithm until it can check what the GCD is. In this case of a sweet, sweet, point addition failure where the GCD is not 1, we can raise an exception which contains the value of the GCD. 

> fade into the chart with the topics 

Remember, the extended Euclidean algorithm doesn't know about the greater context of computing a slope, adding points on an elliptic curve, or even factoring numbers; it just does its job, so this next part is crucial. 

> fade back out

When we raise the exception, control is released from the extended Euclidean algorithm function and the computer is tasked with finding a function that can handle this exception, which can only be one with a try block.

> scroll through functions

It checks the stack from top to bottom. Did the point addition function have a try block? Nope. The double-and-add function? No. Our original function? Yes!

> highlight `except` block

In the case of a raised exception from within the try block, the computer will run the code within the except block. All it takes is a simple check and we have found our factor and can return it after its information has travelled all the way from the extended Euclidean algorithm!

> cycle through images of Hendrik Lenstra until stopping on [this one](https://tse2.mm.bing.net/th?id=OIP.TzI1bE7iA1tXwlvveHtdOgAAAA&pid=Api) when mentioning accomplishment and gradually zooming in

It stands to say that this algorithm, invented by Hendrik Lenstra-- Lenstra's algorithm-- is an *exceptionally* clever algorithm. Perhaps more intriguing is that this algorithm does just fail, but accomplishes its goal by failing the compute a value. If only math tests were like that! Thanks for watching.

> 