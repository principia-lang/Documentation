## Compilation phases

A program consists of statements, each statement declares a function and associates a call.

*NOTE*: In pure CPS, every call is tail call. Therefore, every function body consists of exactly one call. A function can therefore be seen as a mapping from one call to the next. This is why I choose the `↦` symbol to represent a function definition.

```
f a b c ↦ g x y
```

In the above function definition, the function `f` is defined that takes three arguments. In it's body it calls the function `g` with arguments `x` and `y`. 

*NOTE*: Arguments may not be directly used in the call, but can be incorporated through closures.

*NOTE*: The state of execution is entirely contained in the next call and it's arguments. In particular, any data that is not reachable from there is inaccessible.


### Language syntax (unsugared)

#### Example

A program computing the factorial of three is:

```
factorial n return ↦ is_zero n base recurse
base ↦ return 1
recurse ↦ sub n 1 step1
step1 m ↦ fact m step2
step2 f ↦ mul n f return
main exit ↦ factorial 3 exit
```

Numbers, the identifiers `is_zero`, `sub` and `sub` 

#### Disection of a statement

Let's look at the first line of our factorial example program:

Syntactical decomposition

$$
\underbrace{
  \underbrace{
    \code{factorial}
    {\ }
    \code{n}
    {\ }
    \code{return}
  }_{\text{bound variables}}
  \underbrace{
    ↦
  }_{\text{maplet}}
  \underbrace{
    \code{is\_zero}
    {\ }
    \code{n}
    {\ }
    \code{base}
    {\ }
    \code{recurse}
  }_{\text{free variables}}
}_{\text{line}}
$$

Grammatical dissection:

$$
\underbrace{
  \underbrace{
    \underbrace{
      \code{factorial}
    }_{\text{name}}
    {\ }
    \underbrace{
      \code{n}
      {\ }
      \code{return}
    }_{\text{parameters}} 
  }_{\text{function}}
  ↦
  \underbrace{
    \underbrace{
      \code{is\_zero}
    }_{\text{operator}}
    {\ }
    \underbrace{
      \code{n}
      {\ }
      \code{base}
      {\ }
      \code{recurse}
    }_{\text{operands}}
  }_{\text{call}}
}_{\text{procedure}}
$$

Function, routine, subroutine, procedure, abstraction or method?


*NOTE*: The gramatical function (or rather it's name) evaluates to a closure. Similarly, the runtime equivalent of parameters are called 'arguments'. [wiki][WikiParArgs].

[WikiParArgs]: https://en.wikipedia.org/wiki/Parameter_(computer_programming)#Parameters_and_arguments


#### Formal definition

```
Program    ::= Statement*
Statement  ::= Function Arguments "↦" Call Arguments
Function   ::= Identifier
Call       ::= Identifier
Arguments  ::= Identifier*
```

*Note*: This syntax is simplified. The final language will use Unicode based tokenization based on TR31.

[tr31]: http://www.unicode.org/reports/tr31/

In a valid program every `Identifier` only appears once on the left hand side.

A remarkable aspect of this language is that the order of the statements does not matter. Since every non-empty line is a statement, the line-order does not matter. Sources files can be safely passed through `sort` or `shuf` without affecting the final program.

A less remarkable aspect is that the Identifiers do not matter. As long as the definition matches the uses and is unambiguous, it can be changed into anything without changing the meaning of the program. Compare with alpha-equivalence.

An inelegant aspect of the language is that order within statements does matter.

The consequence of these two observations is that the program can be succinctly described as a sort of pseudo-graph. Every statement has an ordered set of outgoing edges, the bound identifiers, and incoming edges, the call. The outgoing edges can split.

TODO: Better graph depiction. Not statements as nodes but identifiers as nodes?

**Example**: The following program computes the factorial of 6. Assuming that `1`, `is_zero`, `sub` and `mul` are defined elsewhere.

```
factorial n return ↦ is_zero n base recurse
base ↦ return 1
recurse ↦ sub n 1 step1
step1 m ↦ fact m step2
step2 f ↦ mul n f return
main result ↦ factorial 3 result
```

After parsing, we have the following program

$$
\begin{align}
P(\code{factorial}) &= \tuple{\array{\code{n}, \code{ret}}, \array{\code{is\_zero}, \code{n}, \code{base}, \code{recurse}}} \\
P(\code{base}) &= \tuple{\array{}, \array{\code{ret}, \code{1}}} \\
P(\code{recurse}) &= \tuple{\array{}, \array{\code{sub}, \code{n}, \code{1}, \code{step1}}} \\
P(\code{step1}) &= \tuple{\array{\code{m}}, \array{\code{factorial}, \code{n}, \code{1}, \code{step2}}} \\
P(\code{step2}) &= \tuple{\array{\code{f}}, \array{\code{mul}, \code{n}, \code{f}, \code{ret}}} \\
P(\code{main}) &= \tuple{\array{\code{exit}}, \array{\code{factorial}, \code{6}, \code{exit}}}
\end{align}
$$

#### Arrays

#### Mappings

We define an update function $U$ that adds to or changes a given function $f$:

$$
U(k, v, f) = x →
\begin{cases}
v & x = k \\
f(x) & \mathrm{otherwise}
\end{cases}
$$

## Operational semantics

$$
\mathsf{builtin}(\text{function})
$$

$$
\mathsf{procedure}(\text{name}, \text{parameters}, \text{operator}, \text{operands})
$$

$$
\mathsf{closure}(\text{procedure}, \text{environment})
$$

$$
\mathsf{apply}(\text{closure}, \text{arguments})
$$



We define an environment $e$ containing pre-defined values and built in functions. We also load the program itself to the environment, encoded as $\mathsf{procedure}$s assigned to the function names.

We define the initial state to be $\mathsf{apply}(\closure{e(\code{main}), e}, \array{\code{exit}})$.

A final state is a state of the form $\mathsf{apply}(\code{exit}, \text{result})$

where $\mathrm{result}$ is the result of the program. 

We define the state transition function $T : \set S → \set S$

The transition for $\code{builtin}$ functions is trivial:

$$
T\ \apply{\builtin{f}, a} = f(a)
$$

Closure are applied as follows. Consider

$$
T\ \apply{c, a}
$$

where

$$
c = \closure{\procedure{n, p, t, r}, e}
$$

1. Extend the environment $e$ to $e'$ by assigning the closure $c$ to the function name $n$ and by assigning every argument in $a$ to it's corresponding parameter in $p$.

2. Set $t' = \mathrm{close}(t, e')$ and similarly map $\mathrm{close}$ over $r$ to obtain $r'$, where
$$
\mathrm{close}(s, e) =
\begin{cases}
\closure{e(s), e} & \mathrm{if } e(s) \text{ is } \mathsf{procedure} \\
e(s) & \mathrm{otherwise}
\end{cases}
\text{.}
$$

3. The new state is $\apply{t', r'}$.

## Example

Consider the following program that computes the cube of three,

```
cube n return ↦ mul n n next
next m ↦ mul n m return
main ret ↦ cube 3 ret
```

When combined with the built in `3` and `mul` this results in the initial environment $e$

$$
\begin{align}
e(\code{cube}) &=
 \procedure{
    \code{cube},
    \array{\code{n}, \code{return}},
    \code{mul},
    \array{\code{n}, \code{n}, \code{next}}
  }
  \text{,}
\\
e(\code{next}) &=
 \procedure{
    \code{next},
    \array{\code{m}},
    \code{mul},
    \array{\code{n}, \code{m}, \code{return}}
  }
  \text{,}
\\
e(\code{main}) &= 
 \procedure{
    \code{main},
    \array{\code{result}},
    \code{cube},
    \array{\code{3}, \code{result}}
  }
  \text{,}
\\
e(\code{mul}) &=
  \builtin{\array{a, b, k} ↦  \apply{k, \array{a · b}}}
  \text{,}
\\
e(\code{3}) &= 3
\text{.}
\end{align}
$$

We can now create the initial state and transition it until we reach a final state:

$$
\begin{align}
&
\apply{
  \closure{e(\code{main}), e},
  \array{\code{exit}}
}
\\&
e' = \{\code{result} → \code{exit}, \code{main} → c_0,  e\}
\\&
\apply{
  \closure{e(\code{cube}), e'},
  \array{3, \code{exit}}
}
\\&
e'' =\{\code{return} → \code{exit}, \code{n} → 3, \code{cube} → c_1,  e'\}
\\&
\apply{
  \mathrm{mul},
  \array{3, 3, \closure{e(\code{next}), e''}}
}
\\&
\apply{
  \closure{e(\code{next}), e''},
  \array{9}
}
\\&
\apply{
  e(\code{mul}),
  \array{3, 9, \code{exit}}
}
\\&
\apply{
  \code{exit},
  \array{27}
}
\end{align}
$$

As can be seen, we carry around many unnecessary variables in the environment. While this is not important for the semantics, and efficient implementation will want to compute minimal closures.

### Language semantics (formal)


Grammar        Runtime
-------------- --------
Symbol         Value
Function name  Closure
Parameters     Arguments
Operator       Closure
Operands       Arguments


Specification: 

The state is an array of values. The compiled program is a mapping from function name to an array of argument indentifiers and an array of call identifiers.
∎

NOTE: Puting this language on formal semantic foundations is hard, because function calls never return by design. Instead, they pass the execution to the next function, which is supplied as an argument. This non-returning breaks both the denotatial semantics (which assumens expresions have values?), and Hoare logic (post-conditions are never reached).

Abstract machine based operational semantics should work though.

http://homepage.divms.uiowa.edu/~slonnegr/plf/Book/Chapter8.pdf

State:

* Program (statements)


The initial expression is “main exit”. The initial environment is $[exit ↦ ]$.

If head(expression) in environment, apply closure to arguments.

else, 


The initial state consists of a closure to evaluate with certain arguments.

First, the first, the closure itself is evaluated. It should resolve to the first identifier of a function.

homepage.divms.uiowa.edu/~slonnegr/plf/Book/

http://homepage.divms.uiowa.edu/~slonnegr/plf/Book/Chapter8.pdf

http://homepages.inf.ed.ac.uk/gdp/publications/sos_jlap.pdf


Post condition:

 * It calls a continuation
 * It calls it satisfying restrictions on the arguments.

```
divmod a b success fail ↦ …
```

Pre conditions:

* a integer
* b non-zero integer
* `success` a function (x₁ x₂) with at most pre-conditions:
  * x₁ integer
	* x₂ integer
	* a = x₁ * b + x₂
	* x₂ < b
* `fail` a function () with at most pre-conditions:
  * b = 0 

Post condition:

* success or fail will be called correctly


[]: http://homepage.divms.uiowa.edu/~slonnegr/plf/Book/Chapter11.pdf


## Namespaces

## Modules

### Imports

```
import Some.Module.Name as SMN
```

The `Some.Module.Name` gets searched for in the module paths as `Some/Module/Name.principia` (or other supported extensions). Exported symbols will be available as `SMN.symbol`.

### Exports

```
export symbolName
```

### Sugared imports 1

```
import Some.Module.Name
```

is shorthand for

```
import Some.Module.Name as Some.Module.Name
```

### Sugared imports 2

```
import Some.Module.Name as .
```

is shorthand for

```
import Some.Module.Name.addition as addition
import Some.Module.Name.multiplication as multiplication
```

... and so on for all exported symbols.

### Sugared imports 3

```
import Some.Module.Name only addition multiplication
```

is shorthand for

```
import Some.Module.Name.addition as addition
import Some.Module.Name.multiplication as multiplication
```

### Sugared exports 1

```
export a b c d
```

is shorthand for

```
export a
export b
export c
export d
```

## Phase 1: The call-graph

All identifiers are bound.

*QUESTION*: When is a graph causally sensible and when is it not?

* Establish closures.
* Constant propagation.
* 


### Phase 2: Virtual machine with explicit reference counting

Instructions:

* `Deref(x)`: Dereferences an argument that will be ingored.
* `Alloc(x₁, …)`: Allocates a new closure.
* `Ref(x, count)`: Increment the reference count on an address by an amount.
* `Call(x₁, …)`:  Tail-calls the given closure with arguments.

These instructions take one or more addresses as arguments:

* `Constant`: The address points to a global constant.
* `Closure`: The address references a local closure variable.
* `Argument`: The address references a local function argument.
* `Alloc`: The address references a just allocated closure.

A function body can contain several `Deref`, `Alloc` and `Ref` instructions, in that order, and finally a single `Call` instruction.


## Syntax sugar

Now that we established the core language, we can add some sugar to make easier to work with, at the cost of complicating the grammar and under-the-hood understanding.

