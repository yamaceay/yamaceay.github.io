---
layout: post
title: "Learn With Me: ReasonML, Part 2"
date: 2024-03-26T23:00:19+00:00
original_url: "https://medium.com/@yamaceay/learn-with-me-reasonml-part-2-6f704e0ded0b"
tags: []
excerpt: "This article requires you to have a basic understanding of ReasonML, a functional programming language which I partly covered in one of my previous articles. How to Learn a Coding Language (Fast) For "
---

<p>This article requires you to have a basic understanding of ReasonML, a functional programming language which I partly covered in one of my previous articles.</p><p><a href="https://yamaceay.medium.com/how-to-learn-a-coding-language-fast-ad7a99eaf375">How to Learn a Coding Language (Fast)</a></p><p>For quick navigation, here are the other articles in the same series:</p><p><a href="https://yamaceay.medium.com/learn-with-me-reasonml-part-1-83b48d9ef694">Learn With Me: ReasonML, Part 1</a></p><p><a href="https://yamaceay.medium.com/learn-with-me-reasonml-part-3-fa246cc034f1">Learn With Me: ReasonML, Part 3</a></p><p>Diving into λ-calculus, you realize it’s foundational for understanding functions as first-class citizens. You can even define natural numbers with just functions, leading us into Church numerals.</p><figure><img alt="" src="https://cdn-images-1.medium.com/max/1400/1*8OY3-7EU1ZD7T1jPcsKfLw.png" /><figcaption>Source: Lambda calculus — Church numerals, Wikipedia</figcaption></figure><p>Here’s the setup:</p><ul><li>“α” stands for a type representing numbers, like “int” in ReasonML.</li><li>You start with an “induction basis”, “x” or “zero”, which is 0.</li><li>Then there’s a “step function”, “f” or “succ”, basically x -&gt; x + 1.</li></ul><p>This way, we can inductively count numbers: “zero” gets you 0, “one” (succ(zero)) is 1, “two” (succ(one)) is 2, and so on.</p><p>In λ-calculus, all natural numbers “n” must satisfy the following type: “∏ α : * . α -&gt; (α -&gt; α) -&gt; α”, which can be read as:</p><blockquote>The type abstraction of α over a function which takes in zero value of type α and successor function of type α -&gt; α and returns a value of type α.</blockquote><p>Now, let’s declare the type of all “natural numbers”:</p><pre><code>nat.re

type natGroup(&#x27;t) = &#x27;t =&gt; (&#x27;t =&gt; &#x27;t) =&gt; &#x27;t;

---

let zero: int = 0;
let succ: int =&gt; int = x =&gt; x + 1;

---

let zeroInt: natGroup(int) = zero =&gt; succ =&gt; zero;
let oneInt: natGroup(int) = zero =&gt; succ =&gt; succ (zero);
let twoInt: natGroup(int) = zero =&gt; succ =&gt; succ (succ (zero));

--- 

zeroInt(zero, succ); oneInt(zero, succ); twoInt(zero, succ);

---

module Nat = {
  type t = int;
  
  let zero: t = 0;
  let succ: t =&gt; t = x =&gt; x + 1;
}

---

Nat.(zero); Nat.(succ(zero)); Nat.(succ(succ(zero)));

---

module type NatGroup = {
  type t;
  
  let zero: t;
  let succ: t =&gt; t;
};

---

module NatPriv: NatGroup = {
  include Nat; 
  let aPrivateMethod = () =&gt; (); // This stays within the module.
};

---

module type ShowNatGroup = {
  include NatGroup;
  let toString: t =&gt; string;
}

---

module ShowNat: ShowNatGroup = {
  include Nat;
  
  let toString = n =&gt; n == zero ? &quot;IsZero&quot; : &quot;IsNotZero&quot;; 
}

---

ShowNat.(zero); ShowNat.(succ(zero)); ShowNat.(succ(succ(zero)));

---

ShowNat.(toString(zero)); ShowNat.(toString(succ(zero)));

---

module type Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let printUntil: int =&gt; unit;
};

---

module Nat: Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let rec getItem = fun
    | 0 =&gt; ShowNatGroup.zero
    | i =&gt; ShowNatGroup.succ(getItem(i - 1));
  
  let printItem = item =&gt; print_endline(ShowNatGroup.toString(item));
  
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? ShowNatGroup.toString(item) : acc ++ &quot;, &quot; ++ ShowNatGroup.toString(item);
  
  let printUntil = n =&gt; {
    let items = List.init(n, getItem);
    print_endline(List.fold_left(join, &quot;&quot;, items));
  };
};

---

module NatInt = Nat({
  type t = int;
  let zero = 0;
  let succ = t =&gt; t + 1;
  let toString = string_of_int;
});

---

module NatBool = Nat({
  type t = bool;
  let zero = false;
  let succ = _ =&gt; true;
  let toString = string_of_bool;
});

---

module NatTern = Nat({
  type t = option(bool);
  let zero = Some(false);
  let succ = fun
    | Some(false) =&gt; None
    | _ =&gt; Some(true);
  let toString = fun
    | Some(item) =&gt; string_of_bool(item)
    | None =&gt; &quot;null&quot;;
});

---

NatBool.printUntil(3);
NatTern.printUntil(3);
NatInt.printUntil(3);

---

module NatChurch = {
  // Here&#x27;s where we get a bit creative with how we combine our Nats.
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? item : item ++ &quot; (&quot; ++ acc ++ &quot;)&quot;;

  // Extending the Nat functor for a specialized case. This is where ReasonML&#x27;s flexibility really shines.
  include Nat({
    type t = list(string);
    let zero = [];
    let succ = t =&gt; [&quot;f&quot;, ...t];
    let toString = t =&gt; List.fold_left(join, &quot;x&quot;, t);
  });
}

---

NatChurch.printUntil(3); 

nat1.re

type natGroup(&#x27;t) = &#x27;t =&gt; (&#x27;t =&gt; &#x27;t) =&gt; &#x27;t;
// type natGroup(&#x27;t) = (&#x27;t, &#x27;t =&gt; &#x27;t) =&gt; &#x27;t;

nat10.re

ShowNat.(zero); ShowNat.(succ(zero)); ShowNat.(succ(succ(zero)));
// - : ShowNat.t = &lt;abstr&gt;
// - : ShowNat.t = &lt;abstr&gt;
// - : ShowNat.t = &lt;abstr&gt;

nat10Real.re

module ShowNat: ShowNatGroup = {
  include Nat;
  
  let toString = n =&gt; n == zero ? &quot;IsZero&quot; : &quot;IsNotZero&quot;; 
}
// module ShowNat: ShowNatGroup;

nat11.re

ShowNat.(toString(zero)); ShowNat.(toString(succ(zero)));
// - : string = &quot;IsZero&quot;
// - : string = &quot;IsNotZero&quot;

nat12.re

module type Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let printUntil: int =&gt; unit;
};
/*
module type Nat =
  (ShowNatGroup : ShowNatGroup) =&gt; { let printUntil: int =&gt; unit; };
*/

nat13.re

module Nat: Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let rec getItem = fun
    | 0 =&gt; ShowNatGroup.zero
    | i =&gt; ShowNatGroup.succ(getItem(i - 1));
  
  let printItem = item =&gt; print_endline(ShowNatGroup.toString(item));
  
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? ShowNatGroup.toString(item) : acc ++ &quot;, &quot; ++ ShowNatGroup.toString(item);
  
  let printUntil = n =&gt; {
    let items = List.init(n, getItem);
    print_endline(List.fold_left(join, &quot;&quot;, items));
  };
};
// module Nat: Nat;

nat14.re

module NatInt = Nat({
  type t = int;
  let zero = 0;
  let succ = t =&gt; t + 1;
  let toString = string_of_int;
});
// module NatInt: { let printUntil: int =&gt; unit; };

nat15.re

module NatBool = Nat({
  type t = bool;
  let zero = false;
  let succ = _ =&gt; true;
  let toString = string_of_bool;
});
// module NatBool: { let printUntil: int =&gt; unit; };

nat16.re

module NatTern = Nat({
  type t = option(bool);
  let zero = Some(false);
  let succ = fun
    | Some(false) =&gt; None
    | _ =&gt; Some(true);
  let toString = fun
    | Some(item) =&gt; string_of_bool(item)
    | None =&gt; &quot;null&quot;;
});
// module NatTern: { let printUntil: int =&gt; unit; };

nat17.re

NatBool.printUntil(3);
// false, true, true

NatTern.printUntil(3);
// false, null, true

NatInt.printUntil(3);
// 0, 1, 2

nat18.re

module NatChurch = {
  // Here&#x27;s where we get a bit creative with how we combine our Nats.
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? item : item ++ &quot; (&quot; ++ acc ++ &quot;)&quot;;

  // Extending the Nat functor for a specialized case. This is where ReasonML&#x27;s flexibility really shines.
  include Nat({
    type t = list(string);
    let zero = [];
    let succ = t =&gt; [&quot;f&quot;, ...t];
    let toString = t =&gt; List.fold_left(join, &quot;x&quot;, t);
  });
}
/* 
module NatChurch:
  { let join: (string, string) =&gt; string; let printUntil: int =&gt; unit; };
*/

nat19.re

NatChurch.printUntil(3);
// x, f (x), f (f (x))

nat2.re

let zero: int = 0;
// let zero: int = 0;

let succ: int =&gt; int = x =&gt; x + 1;
// let succ: int =&gt; int = &lt;fun&gt;;

nat3.re

let zeroInt: natGroup(int) = zero =&gt; succ =&gt; zero;
// let zeroInt: natGroup(int) = &lt;fun&gt;;

let oneInt: natGroup(int) = zero =&gt; succ =&gt; succ (zero);
// let oneInt: natGroup(int) = &lt;fun&gt;;

let twoInt: natGroup(int) = zero =&gt; succ =&gt; succ (succ (zero));
// let twoInt: natGroup(int) = &lt;fun&gt;;

nat4.re

zeroInt(zero, succ); oneInt(zero, succ); twoInt(zero, succ);
// - : int = 0
// - : int = 1
// - : int = 2

nat5.re

module Nat = {
  type t = int;
  
  let zero: t = 0;
  let succ: t =&gt; t = x =&gt; x + 1;
}
// module Nat: { type t = int; let zero: t; let succ: t =&gt; t; };

nat6.re

Nat.(zero); Nat.(succ(zero)); Nat.(succ(succ(zero)));
// - : Nat.t = 0
// - : Nat.t = 1
// - : Nat.t = 2

nat7.re

module type NatGroup = {
  type t;
  
  let zero: t;
  let succ: t =&gt; t;
};
// module type NatGroup = { type t; let zero: t; let succ: t =&gt; t; };

nat8.re

module NatPriv: NatGroup = {
  include Nat; 
  let aPrivateMethod = () =&gt; (); // This stays within the module.
};
// module NatPriv: NatGroup;

nat9.re

module type ShowNatGroup = {
  include NatGroup;
  let toString: t =&gt; string;
}
/* 
module type ShowNatGroup =
  { type t; let zero: t; let succ: t =&gt; t; let toString: t =&gt; string; };
*/</code></pre><p>Implementing natural numbers in ReasonML using natGroup is straightforward:</p><pre><code>nat.re

type natGroup(&#x27;t) = &#x27;t =&gt; (&#x27;t =&gt; &#x27;t) =&gt; &#x27;t;

---

let zero: int = 0;
let succ: int =&gt; int = x =&gt; x + 1;

---

let zeroInt: natGroup(int) = zero =&gt; succ =&gt; zero;
let oneInt: natGroup(int) = zero =&gt; succ =&gt; succ (zero);
let twoInt: natGroup(int) = zero =&gt; succ =&gt; succ (succ (zero));

--- 

zeroInt(zero, succ); oneInt(zero, succ); twoInt(zero, succ);

---

module Nat = {
  type t = int;
  
  let zero: t = 0;
  let succ: t =&gt; t = x =&gt; x + 1;
}

---

Nat.(zero); Nat.(succ(zero)); Nat.(succ(succ(zero)));

---

module type NatGroup = {
  type t;
  
  let zero: t;
  let succ: t =&gt; t;
};

---

module NatPriv: NatGroup = {
  include Nat; 
  let aPrivateMethod = () =&gt; (); // This stays within the module.
};

---

module type ShowNatGroup = {
  include NatGroup;
  let toString: t =&gt; string;
}

---

module ShowNat: ShowNatGroup = {
  include Nat;
  
  let toString = n =&gt; n == zero ? &quot;IsZero&quot; : &quot;IsNotZero&quot;; 
}

---

ShowNat.(zero); ShowNat.(succ(zero)); ShowNat.(succ(succ(zero)));

---

ShowNat.(toString(zero)); ShowNat.(toString(succ(zero)));

---

module type Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let printUntil: int =&gt; unit;
};

---

module Nat: Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let rec getItem = fun
    | 0 =&gt; ShowNatGroup.zero
    | i =&gt; ShowNatGroup.succ(getItem(i - 1));
  
  let printItem = item =&gt; print_endline(ShowNatGroup.toString(item));
  
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? ShowNatGroup.toString(item) : acc ++ &quot;, &quot; ++ ShowNatGroup.toString(item);
  
  let printUntil = n =&gt; {
    let items = List.init(n, getItem);
    print_endline(List.fold_left(join, &quot;&quot;, items));
  };
};

---

module NatInt = Nat({
  type t = int;
  let zero = 0;
  let succ = t =&gt; t + 1;
  let toString = string_of_int;
});

---

module NatBool = Nat({
  type t = bool;
  let zero = false;
  let succ = _ =&gt; true;
  let toString = string_of_bool;
});

---

module NatTern = Nat({
  type t = option(bool);
  let zero = Some(false);
  let succ = fun
    | Some(false) =&gt; None
    | _ =&gt; Some(true);
  let toString = fun
    | Some(item) =&gt; string_of_bool(item)
    | None =&gt; &quot;null&quot;;
});

---

NatBool.printUntil(3);
NatTern.printUntil(3);
NatInt.printUntil(3);

---

module NatChurch = {
  // Here&#x27;s where we get a bit creative with how we combine our Nats.
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? item : item ++ &quot; (&quot; ++ acc ++ &quot;)&quot;;

  // Extending the Nat functor for a specialized case. This is where ReasonML&#x27;s flexibility really shines.
  include Nat({
    type t = list(string);
    let zero = [];
    let succ = t =&gt; [&quot;f&quot;, ...t];
    let toString = t =&gt; List.fold_left(join, &quot;x&quot;, t);
  });
}

---

NatChurch.printUntil(3); 

nat1.re

type natGroup(&#x27;t) = &#x27;t =&gt; (&#x27;t =&gt; &#x27;t) =&gt; &#x27;t;
// type natGroup(&#x27;t) = (&#x27;t, &#x27;t =&gt; &#x27;t) =&gt; &#x27;t;

nat10.re

ShowNat.(zero); ShowNat.(succ(zero)); ShowNat.(succ(succ(zero)));
// - : ShowNat.t = &lt;abstr&gt;
// - : ShowNat.t = &lt;abstr&gt;
// - : ShowNat.t = &lt;abstr&gt;

nat10Real.re

module ShowNat: ShowNatGroup = {
  include Nat;
  
  let toString = n =&gt; n == zero ? &quot;IsZero&quot; : &quot;IsNotZero&quot;; 
}
// module ShowNat: ShowNatGroup;

nat11.re

ShowNat.(toString(zero)); ShowNat.(toString(succ(zero)));
// - : string = &quot;IsZero&quot;
// - : string = &quot;IsNotZero&quot;

nat12.re

module type Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let printUntil: int =&gt; unit;
};
/*
module type Nat =
  (ShowNatGroup : ShowNatGroup) =&gt; { let printUntil: int =&gt; unit; };
*/

nat13.re

module Nat: Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let rec getItem = fun
    | 0 =&gt; ShowNatGroup.zero
    | i =&gt; ShowNatGroup.succ(getItem(i - 1));
  
  let printItem = item =&gt; print_endline(ShowNatGroup.toString(item));
  
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? ShowNatGroup.toString(item) : acc ++ &quot;, &quot; ++ ShowNatGroup.toString(item);
  
  let printUntil = n =&gt; {
    let items = List.init(n, getItem);
    print_endline(List.fold_left(join, &quot;&quot;, items));
  };
};
// module Nat: Nat;

nat14.re

module NatInt = Nat({
  type t = int;
  let zero = 0;
  let succ = t =&gt; t + 1;
  let toString = string_of_int;
});
// module NatInt: { let printUntil: int =&gt; unit; };

nat15.re

module NatBool = Nat({
  type t = bool;
  let zero = false;
  let succ = _ =&gt; true;
  let toString = string_of_bool;
});
// module NatBool: { let printUntil: int =&gt; unit; };

nat16.re

module NatTern = Nat({
  type t = option(bool);
  let zero = Some(false);
  let succ = fun
    | Some(false) =&gt; None
    | _ =&gt; Some(true);
  let toString = fun
    | Some(item) =&gt; string_of_bool(item)
    | None =&gt; &quot;null&quot;;
});
// module NatTern: { let printUntil: int =&gt; unit; };

nat17.re

NatBool.printUntil(3);
// false, true, true

NatTern.printUntil(3);
// false, null, true

NatInt.printUntil(3);
// 0, 1, 2

nat18.re

module NatChurch = {
  // Here&#x27;s where we get a bit creative with how we combine our Nats.
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? item : item ++ &quot; (&quot; ++ acc ++ &quot;)&quot;;

  // Extending the Nat functor for a specialized case. This is where ReasonML&#x27;s flexibility really shines.
  include Nat({
    type t = list(string);
    let zero = [];
    let succ = t =&gt; [&quot;f&quot;, ...t];
    let toString = t =&gt; List.fold_left(join, &quot;x&quot;, t);
  });
}
/* 
module NatChurch:
  { let join: (string, string) =&gt; string; let printUntil: int =&gt; unit; };
*/

nat19.re

NatChurch.printUntil(3);
// x, f (x), f (f (x))

nat2.re

let zero: int = 0;
// let zero: int = 0;

let succ: int =&gt; int = x =&gt; x + 1;
// let succ: int =&gt; int = &lt;fun&gt;;

nat3.re

let zeroInt: natGroup(int) = zero =&gt; succ =&gt; zero;
// let zeroInt: natGroup(int) = &lt;fun&gt;;

let oneInt: natGroup(int) = zero =&gt; succ =&gt; succ (zero);
// let oneInt: natGroup(int) = &lt;fun&gt;;

let twoInt: natGroup(int) = zero =&gt; succ =&gt; succ (succ (zero));
// let twoInt: natGroup(int) = &lt;fun&gt;;

nat4.re

zeroInt(zero, succ); oneInt(zero, succ); twoInt(zero, succ);
// - : int = 0
// - : int = 1
// - : int = 2

nat5.re

module Nat = {
  type t = int;
  
  let zero: t = 0;
  let succ: t =&gt; t = x =&gt; x + 1;
}
// module Nat: { type t = int; let zero: t; let succ: t =&gt; t; };

nat6.re

Nat.(zero); Nat.(succ(zero)); Nat.(succ(succ(zero)));
// - : Nat.t = 0
// - : Nat.t = 1
// - : Nat.t = 2

nat7.re

module type NatGroup = {
  type t;
  
  let zero: t;
  let succ: t =&gt; t;
};
// module type NatGroup = { type t; let zero: t; let succ: t =&gt; t; };

nat8.re

module NatPriv: NatGroup = {
  include Nat; 
  let aPrivateMethod = () =&gt; (); // This stays within the module.
};
// module NatPriv: NatGroup;

nat9.re

module type ShowNatGroup = {
  include NatGroup;
  let toString: t =&gt; string;
}
/* 
module type ShowNatGroup =
  { type t; let zero: t; let succ: t =&gt; t; let toString: t =&gt; string; };
*/</code></pre><p>Typed church numerals look like this:</p><pre><code>nat.re

type natGroup(&#x27;t) = &#x27;t =&gt; (&#x27;t =&gt; &#x27;t) =&gt; &#x27;t;

---

let zero: int = 0;
let succ: int =&gt; int = x =&gt; x + 1;

---

let zeroInt: natGroup(int) = zero =&gt; succ =&gt; zero;
let oneInt: natGroup(int) = zero =&gt; succ =&gt; succ (zero);
let twoInt: natGroup(int) = zero =&gt; succ =&gt; succ (succ (zero));

--- 

zeroInt(zero, succ); oneInt(zero, succ); twoInt(zero, succ);

---

module Nat = {
  type t = int;
  
  let zero: t = 0;
  let succ: t =&gt; t = x =&gt; x + 1;
}

---

Nat.(zero); Nat.(succ(zero)); Nat.(succ(succ(zero)));

---

module type NatGroup = {
  type t;
  
  let zero: t;
  let succ: t =&gt; t;
};

---

module NatPriv: NatGroup = {
  include Nat; 
  let aPrivateMethod = () =&gt; (); // This stays within the module.
};

---

module type ShowNatGroup = {
  include NatGroup;
  let toString: t =&gt; string;
}

---

module ShowNat: ShowNatGroup = {
  include Nat;
  
  let toString = n =&gt; n == zero ? &quot;IsZero&quot; : &quot;IsNotZero&quot;; 
}

---

ShowNat.(zero); ShowNat.(succ(zero)); ShowNat.(succ(succ(zero)));

---

ShowNat.(toString(zero)); ShowNat.(toString(succ(zero)));

---

module type Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let printUntil: int =&gt; unit;
};

---

module Nat: Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let rec getItem = fun
    | 0 =&gt; ShowNatGroup.zero
    | i =&gt; ShowNatGroup.succ(getItem(i - 1));
  
  let printItem = item =&gt; print_endline(ShowNatGroup.toString(item));
  
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? ShowNatGroup.toString(item) : acc ++ &quot;, &quot; ++ ShowNatGroup.toString(item);
  
  let printUntil = n =&gt; {
    let items = List.init(n, getItem);
    print_endline(List.fold_left(join, &quot;&quot;, items));
  };
};

---

module NatInt = Nat({
  type t = int;
  let zero = 0;
  let succ = t =&gt; t + 1;
  let toString = string_of_int;
});

---

module NatBool = Nat({
  type t = bool;
  let zero = false;
  let succ = _ =&gt; true;
  let toString = string_of_bool;
});

---

module NatTern = Nat({
  type t = option(bool);
  let zero = Some(false);
  let succ = fun
    | Some(false) =&gt; None
    | _ =&gt; Some(true);
  let toString = fun
    | Some(item) =&gt; string_of_bool(item)
    | None =&gt; &quot;null&quot;;
});

---

NatBool.printUntil(3);
NatTern.printUntil(3);
NatInt.printUntil(3);

---

module NatChurch = {
  // Here&#x27;s where we get a bit creative with how we combine our Nats.
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? item : item ++ &quot; (&quot; ++ acc ++ &quot;)&quot;;

  // Extending the Nat functor for a specialized case. This is where ReasonML&#x27;s flexibility really shines.
  include Nat({
    type t = list(string);
    let zero = [];
    let succ = t =&gt; [&quot;f&quot;, ...t];
    let toString = t =&gt; List.fold_left(join, &quot;x&quot;, t);
  });
}

---

NatChurch.printUntil(3); 

nat1.re

type natGroup(&#x27;t) = &#x27;t =&gt; (&#x27;t =&gt; &#x27;t) =&gt; &#x27;t;
// type natGroup(&#x27;t) = (&#x27;t, &#x27;t =&gt; &#x27;t) =&gt; &#x27;t;

nat10.re

ShowNat.(zero); ShowNat.(succ(zero)); ShowNat.(succ(succ(zero)));
// - : ShowNat.t = &lt;abstr&gt;
// - : ShowNat.t = &lt;abstr&gt;
// - : ShowNat.t = &lt;abstr&gt;

nat10Real.re

module ShowNat: ShowNatGroup = {
  include Nat;
  
  let toString = n =&gt; n == zero ? &quot;IsZero&quot; : &quot;IsNotZero&quot;; 
}
// module ShowNat: ShowNatGroup;

nat11.re

ShowNat.(toString(zero)); ShowNat.(toString(succ(zero)));
// - : string = &quot;IsZero&quot;
// - : string = &quot;IsNotZero&quot;

nat12.re

module type Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let printUntil: int =&gt; unit;
};
/*
module type Nat =
  (ShowNatGroup : ShowNatGroup) =&gt; { let printUntil: int =&gt; unit; };
*/

nat13.re

module Nat: Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let rec getItem = fun
    | 0 =&gt; ShowNatGroup.zero
    | i =&gt; ShowNatGroup.succ(getItem(i - 1));
  
  let printItem = item =&gt; print_endline(ShowNatGroup.toString(item));
  
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? ShowNatGroup.toString(item) : acc ++ &quot;, &quot; ++ ShowNatGroup.toString(item);
  
  let printUntil = n =&gt; {
    let items = List.init(n, getItem);
    print_endline(List.fold_left(join, &quot;&quot;, items));
  };
};
// module Nat: Nat;

nat14.re

module NatInt = Nat({
  type t = int;
  let zero = 0;
  let succ = t =&gt; t + 1;
  let toString = string_of_int;
});
// module NatInt: { let printUntil: int =&gt; unit; };

nat15.re

module NatBool = Nat({
  type t = bool;
  let zero = false;
  let succ = _ =&gt; true;
  let toString = string_of_bool;
});
// module NatBool: { let printUntil: int =&gt; unit; };

nat16.re

module NatTern = Nat({
  type t = option(bool);
  let zero = Some(false);
  let succ = fun
    | Some(false) =&gt; None
    | _ =&gt; Some(true);
  let toString = fun
    | Some(item) =&gt; string_of_bool(item)
    | None =&gt; &quot;null&quot;;
});
// module NatTern: { let printUntil: int =&gt; unit; };

nat17.re

NatBool.printUntil(3);
// false, true, true

NatTern.printUntil(3);
// false, null, true

NatInt.printUntil(3);
// 0, 1, 2

nat18.re

module NatChurch = {
  // Here&#x27;s where we get a bit creative with how we combine our Nats.
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? item : item ++ &quot; (&quot; ++ acc ++ &quot;)&quot;;

  // Extending the Nat functor for a specialized case. This is where ReasonML&#x27;s flexibility really shines.
  include Nat({
    type t = list(string);
    let zero = [];
    let succ = t =&gt; [&quot;f&quot;, ...t];
    let toString = t =&gt; List.fold_left(join, &quot;x&quot;, t);
  });
}
/* 
module NatChurch:
  { let join: (string, string) =&gt; string; let printUntil: int =&gt; unit; };
*/

nat19.re

NatChurch.printUntil(3);
// x, f (x), f (f (x))

nat2.re

let zero: int = 0;
// let zero: int = 0;

let succ: int =&gt; int = x =&gt; x + 1;
// let succ: int =&gt; int = &lt;fun&gt;;

nat3.re

let zeroInt: natGroup(int) = zero =&gt; succ =&gt; zero;
// let zeroInt: natGroup(int) = &lt;fun&gt;;

let oneInt: natGroup(int) = zero =&gt; succ =&gt; succ (zero);
// let oneInt: natGroup(int) = &lt;fun&gt;;

let twoInt: natGroup(int) = zero =&gt; succ =&gt; succ (succ (zero));
// let twoInt: natGroup(int) = &lt;fun&gt;;

nat4.re

zeroInt(zero, succ); oneInt(zero, succ); twoInt(zero, succ);
// - : int = 0
// - : int = 1
// - : int = 2

nat5.re

module Nat = {
  type t = int;
  
  let zero: t = 0;
  let succ: t =&gt; t = x =&gt; x + 1;
}
// module Nat: { type t = int; let zero: t; let succ: t =&gt; t; };

nat6.re

Nat.(zero); Nat.(succ(zero)); Nat.(succ(succ(zero)));
// - : Nat.t = 0
// - : Nat.t = 1
// - : Nat.t = 2

nat7.re

module type NatGroup = {
  type t;
  
  let zero: t;
  let succ: t =&gt; t;
};
// module type NatGroup = { type t; let zero: t; let succ: t =&gt; t; };

nat8.re

module NatPriv: NatGroup = {
  include Nat; 
  let aPrivateMethod = () =&gt; (); // This stays within the module.
};
// module NatPriv: NatGroup;

nat9.re

module type ShowNatGroup = {
  include NatGroup;
  let toString: t =&gt; string;
}
/* 
module type ShowNatGroup =
  { type t; let zero: t; let succ: t =&gt; t; let toString: t =&gt; string; };
*/</code></pre><p>When fully evaluated, these church numerals yield natural numbers.</p><pre><code>nat.re

type natGroup(&#x27;t) = &#x27;t =&gt; (&#x27;t =&gt; &#x27;t) =&gt; &#x27;t;

---

let zero: int = 0;
let succ: int =&gt; int = x =&gt; x + 1;

---

let zeroInt: natGroup(int) = zero =&gt; succ =&gt; zero;
let oneInt: natGroup(int) = zero =&gt; succ =&gt; succ (zero);
let twoInt: natGroup(int) = zero =&gt; succ =&gt; succ (succ (zero));

--- 

zeroInt(zero, succ); oneInt(zero, succ); twoInt(zero, succ);

---

module Nat = {
  type t = int;
  
  let zero: t = 0;
  let succ: t =&gt; t = x =&gt; x + 1;
}

---

Nat.(zero); Nat.(succ(zero)); Nat.(succ(succ(zero)));

---

module type NatGroup = {
  type t;
  
  let zero: t;
  let succ: t =&gt; t;
};

---

module NatPriv: NatGroup = {
  include Nat; 
  let aPrivateMethod = () =&gt; (); // This stays within the module.
};

---

module type ShowNatGroup = {
  include NatGroup;
  let toString: t =&gt; string;
}

---

module ShowNat: ShowNatGroup = {
  include Nat;
  
  let toString = n =&gt; n == zero ? &quot;IsZero&quot; : &quot;IsNotZero&quot;; 
}

---

ShowNat.(zero); ShowNat.(succ(zero)); ShowNat.(succ(succ(zero)));

---

ShowNat.(toString(zero)); ShowNat.(toString(succ(zero)));

---

module type Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let printUntil: int =&gt; unit;
};

---

module Nat: Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let rec getItem = fun
    | 0 =&gt; ShowNatGroup.zero
    | i =&gt; ShowNatGroup.succ(getItem(i - 1));
  
  let printItem = item =&gt; print_endline(ShowNatGroup.toString(item));
  
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? ShowNatGroup.toString(item) : acc ++ &quot;, &quot; ++ ShowNatGroup.toString(item);
  
  let printUntil = n =&gt; {
    let items = List.init(n, getItem);
    print_endline(List.fold_left(join, &quot;&quot;, items));
  };
};

---

module NatInt = Nat({
  type t = int;
  let zero = 0;
  let succ = t =&gt; t + 1;
  let toString = string_of_int;
});

---

module NatBool = Nat({
  type t = bool;
  let zero = false;
  let succ = _ =&gt; true;
  let toString = string_of_bool;
});

---

module NatTern = Nat({
  type t = option(bool);
  let zero = Some(false);
  let succ = fun
    | Some(false) =&gt; None
    | _ =&gt; Some(true);
  let toString = fun
    | Some(item) =&gt; string_of_bool(item)
    | None =&gt; &quot;null&quot;;
});

---

NatBool.printUntil(3);
NatTern.printUntil(3);
NatInt.printUntil(3);

---

module NatChurch = {
  // Here&#x27;s where we get a bit creative with how we combine our Nats.
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? item : item ++ &quot; (&quot; ++ acc ++ &quot;)&quot;;

  // Extending the Nat functor for a specialized case. This is where ReasonML&#x27;s flexibility really shines.
  include Nat({
    type t = list(string);
    let zero = [];
    let succ = t =&gt; [&quot;f&quot;, ...t];
    let toString = t =&gt; List.fold_left(join, &quot;x&quot;, t);
  });
}

---

NatChurch.printUntil(3); 

nat1.re

type natGroup(&#x27;t) = &#x27;t =&gt; (&#x27;t =&gt; &#x27;t) =&gt; &#x27;t;
// type natGroup(&#x27;t) = (&#x27;t, &#x27;t =&gt; &#x27;t) =&gt; &#x27;t;

nat10.re

ShowNat.(zero); ShowNat.(succ(zero)); ShowNat.(succ(succ(zero)));
// - : ShowNat.t = &lt;abstr&gt;
// - : ShowNat.t = &lt;abstr&gt;
// - : ShowNat.t = &lt;abstr&gt;

nat10Real.re

module ShowNat: ShowNatGroup = {
  include Nat;
  
  let toString = n =&gt; n == zero ? &quot;IsZero&quot; : &quot;IsNotZero&quot;; 
}
// module ShowNat: ShowNatGroup;

nat11.re

ShowNat.(toString(zero)); ShowNat.(toString(succ(zero)));
// - : string = &quot;IsZero&quot;
// - : string = &quot;IsNotZero&quot;

nat12.re

module type Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let printUntil: int =&gt; unit;
};
/*
module type Nat =
  (ShowNatGroup : ShowNatGroup) =&gt; { let printUntil: int =&gt; unit; };
*/

nat13.re

module Nat: Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let rec getItem = fun
    | 0 =&gt; ShowNatGroup.zero
    | i =&gt; ShowNatGroup.succ(getItem(i - 1));
  
  let printItem = item =&gt; print_endline(ShowNatGroup.toString(item));
  
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? ShowNatGroup.toString(item) : acc ++ &quot;, &quot; ++ ShowNatGroup.toString(item);
  
  let printUntil = n =&gt; {
    let items = List.init(n, getItem);
    print_endline(List.fold_left(join, &quot;&quot;, items));
  };
};
// module Nat: Nat;

nat14.re

module NatInt = Nat({
  type t = int;
  let zero = 0;
  let succ = t =&gt; t + 1;
  let toString = string_of_int;
});
// module NatInt: { let printUntil: int =&gt; unit; };

nat15.re

module NatBool = Nat({
  type t = bool;
  let zero = false;
  let succ = _ =&gt; true;
  let toString = string_of_bool;
});
// module NatBool: { let printUntil: int =&gt; unit; };

nat16.re

module NatTern = Nat({
  type t = option(bool);
  let zero = Some(false);
  let succ = fun
    | Some(false) =&gt; None
    | _ =&gt; Some(true);
  let toString = fun
    | Some(item) =&gt; string_of_bool(item)
    | None =&gt; &quot;null&quot;;
});
// module NatTern: { let printUntil: int =&gt; unit; };

nat17.re

NatBool.printUntil(3);
// false, true, true

NatTern.printUntil(3);
// false, null, true

NatInt.printUntil(3);
// 0, 1, 2

nat18.re

module NatChurch = {
  // Here&#x27;s where we get a bit creative with how we combine our Nats.
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? item : item ++ &quot; (&quot; ++ acc ++ &quot;)&quot;;

  // Extending the Nat functor for a specialized case. This is where ReasonML&#x27;s flexibility really shines.
  include Nat({
    type t = list(string);
    let zero = [];
    let succ = t =&gt; [&quot;f&quot;, ...t];
    let toString = t =&gt; List.fold_left(join, &quot;x&quot;, t);
  });
}
/* 
module NatChurch:
  { let join: (string, string) =&gt; string; let printUntil: int =&gt; unit; };
*/

nat19.re

NatChurch.printUntil(3);
// x, f (x), f (f (x))

nat2.re

let zero: int = 0;
// let zero: int = 0;

let succ: int =&gt; int = x =&gt; x + 1;
// let succ: int =&gt; int = &lt;fun&gt;;

nat3.re

let zeroInt: natGroup(int) = zero =&gt; succ =&gt; zero;
// let zeroInt: natGroup(int) = &lt;fun&gt;;

let oneInt: natGroup(int) = zero =&gt; succ =&gt; succ (zero);
// let oneInt: natGroup(int) = &lt;fun&gt;;

let twoInt: natGroup(int) = zero =&gt; succ =&gt; succ (succ (zero));
// let twoInt: natGroup(int) = &lt;fun&gt;;

nat4.re

zeroInt(zero, succ); oneInt(zero, succ); twoInt(zero, succ);
// - : int = 0
// - : int = 1
// - : int = 2

nat5.re

module Nat = {
  type t = int;
  
  let zero: t = 0;
  let succ: t =&gt; t = x =&gt; x + 1;
}
// module Nat: { type t = int; let zero: t; let succ: t =&gt; t; };

nat6.re

Nat.(zero); Nat.(succ(zero)); Nat.(succ(succ(zero)));
// - : Nat.t = 0
// - : Nat.t = 1
// - : Nat.t = 2

nat7.re

module type NatGroup = {
  type t;
  
  let zero: t;
  let succ: t =&gt; t;
};
// module type NatGroup = { type t; let zero: t; let succ: t =&gt; t; };

nat8.re

module NatPriv: NatGroup = {
  include Nat; 
  let aPrivateMethod = () =&gt; (); // This stays within the module.
};
// module NatPriv: NatGroup;

nat9.re

module type ShowNatGroup = {
  include NatGroup;
  let toString: t =&gt; string;
}
/* 
module type ShowNatGroup =
  { type t; let zero: t; let succ: t =&gt; t; let toString: t =&gt; string; };
*/</code></pre><p>The trick was getting polymorphism right. Initially, types and terms had to be explicitly linear, which was a bit limiting. Wrapping the definitions in a local scope helped abstract away the complexity.</p><pre><code>nat.re

type natGroup(&#x27;t) = &#x27;t =&gt; (&#x27;t =&gt; &#x27;t) =&gt; &#x27;t;

---

let zero: int = 0;
let succ: int =&gt; int = x =&gt; x + 1;

---

let zeroInt: natGroup(int) = zero =&gt; succ =&gt; zero;
let oneInt: natGroup(int) = zero =&gt; succ =&gt; succ (zero);
let twoInt: natGroup(int) = zero =&gt; succ =&gt; succ (succ (zero));

--- 

zeroInt(zero, succ); oneInt(zero, succ); twoInt(zero, succ);

---

module Nat = {
  type t = int;
  
  let zero: t = 0;
  let succ: t =&gt; t = x =&gt; x + 1;
}

---

Nat.(zero); Nat.(succ(zero)); Nat.(succ(succ(zero)));

---

module type NatGroup = {
  type t;
  
  let zero: t;
  let succ: t =&gt; t;
};

---

module NatPriv: NatGroup = {
  include Nat; 
  let aPrivateMethod = () =&gt; (); // This stays within the module.
};

---

module type ShowNatGroup = {
  include NatGroup;
  let toString: t =&gt; string;
}

---

module ShowNat: ShowNatGroup = {
  include Nat;
  
  let toString = n =&gt; n == zero ? &quot;IsZero&quot; : &quot;IsNotZero&quot;; 
}

---

ShowNat.(zero); ShowNat.(succ(zero)); ShowNat.(succ(succ(zero)));

---

ShowNat.(toString(zero)); ShowNat.(toString(succ(zero)));

---

module type Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let printUntil: int =&gt; unit;
};

---

module Nat: Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let rec getItem = fun
    | 0 =&gt; ShowNatGroup.zero
    | i =&gt; ShowNatGroup.succ(getItem(i - 1));
  
  let printItem = item =&gt; print_endline(ShowNatGroup.toString(item));
  
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? ShowNatGroup.toString(item) : acc ++ &quot;, &quot; ++ ShowNatGroup.toString(item);
  
  let printUntil = n =&gt; {
    let items = List.init(n, getItem);
    print_endline(List.fold_left(join, &quot;&quot;, items));
  };
};

---

module NatInt = Nat({
  type t = int;
  let zero = 0;
  let succ = t =&gt; t + 1;
  let toString = string_of_int;
});

---

module NatBool = Nat({
  type t = bool;
  let zero = false;
  let succ = _ =&gt; true;
  let toString = string_of_bool;
});

---

module NatTern = Nat({
  type t = option(bool);
  let zero = Some(false);
  let succ = fun
    | Some(false) =&gt; None
    | _ =&gt; Some(true);
  let toString = fun
    | Some(item) =&gt; string_of_bool(item)
    | None =&gt; &quot;null&quot;;
});

---

NatBool.printUntil(3);
NatTern.printUntil(3);
NatInt.printUntil(3);

---

module NatChurch = {
  // Here&#x27;s where we get a bit creative with how we combine our Nats.
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? item : item ++ &quot; (&quot; ++ acc ++ &quot;)&quot;;

  // Extending the Nat functor for a specialized case. This is where ReasonML&#x27;s flexibility really shines.
  include Nat({
    type t = list(string);
    let zero = [];
    let succ = t =&gt; [&quot;f&quot;, ...t];
    let toString = t =&gt; List.fold_left(join, &quot;x&quot;, t);
  });
}

---

NatChurch.printUntil(3); 

nat1.re

type natGroup(&#x27;t) = &#x27;t =&gt; (&#x27;t =&gt; &#x27;t) =&gt; &#x27;t;
// type natGroup(&#x27;t) = (&#x27;t, &#x27;t =&gt; &#x27;t) =&gt; &#x27;t;

nat10.re

ShowNat.(zero); ShowNat.(succ(zero)); ShowNat.(succ(succ(zero)));
// - : ShowNat.t = &lt;abstr&gt;
// - : ShowNat.t = &lt;abstr&gt;
// - : ShowNat.t = &lt;abstr&gt;

nat10Real.re

module ShowNat: ShowNatGroup = {
  include Nat;
  
  let toString = n =&gt; n == zero ? &quot;IsZero&quot; : &quot;IsNotZero&quot;; 
}
// module ShowNat: ShowNatGroup;

nat11.re

ShowNat.(toString(zero)); ShowNat.(toString(succ(zero)));
// - : string = &quot;IsZero&quot;
// - : string = &quot;IsNotZero&quot;

nat12.re

module type Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let printUntil: int =&gt; unit;
};
/*
module type Nat =
  (ShowNatGroup : ShowNatGroup) =&gt; { let printUntil: int =&gt; unit; };
*/

nat13.re

module Nat: Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let rec getItem = fun
    | 0 =&gt; ShowNatGroup.zero
    | i =&gt; ShowNatGroup.succ(getItem(i - 1));
  
  let printItem = item =&gt; print_endline(ShowNatGroup.toString(item));
  
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? ShowNatGroup.toString(item) : acc ++ &quot;, &quot; ++ ShowNatGroup.toString(item);
  
  let printUntil = n =&gt; {
    let items = List.init(n, getItem);
    print_endline(List.fold_left(join, &quot;&quot;, items));
  };
};
// module Nat: Nat;

nat14.re

module NatInt = Nat({
  type t = int;
  let zero = 0;
  let succ = t =&gt; t + 1;
  let toString = string_of_int;
});
// module NatInt: { let printUntil: int =&gt; unit; };

nat15.re

module NatBool = Nat({
  type t = bool;
  let zero = false;
  let succ = _ =&gt; true;
  let toString = string_of_bool;
});
// module NatBool: { let printUntil: int =&gt; unit; };

nat16.re

module NatTern = Nat({
  type t = option(bool);
  let zero = Some(false);
  let succ = fun
    | Some(false) =&gt; None
    | _ =&gt; Some(true);
  let toString = fun
    | Some(item) =&gt; string_of_bool(item)
    | None =&gt; &quot;null&quot;;
});
// module NatTern: { let printUntil: int =&gt; unit; };

nat17.re

NatBool.printUntil(3);
// false, true, true

NatTern.printUntil(3);
// false, null, true

NatInt.printUntil(3);
// 0, 1, 2

nat18.re

module NatChurch = {
  // Here&#x27;s where we get a bit creative with how we combine our Nats.
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? item : item ++ &quot; (&quot; ++ acc ++ &quot;)&quot;;

  // Extending the Nat functor for a specialized case. This is where ReasonML&#x27;s flexibility really shines.
  include Nat({
    type t = list(string);
    let zero = [];
    let succ = t =&gt; [&quot;f&quot;, ...t];
    let toString = t =&gt; List.fold_left(join, &quot;x&quot;, t);
  });
}
/* 
module NatChurch:
  { let join: (string, string) =&gt; string; let printUntil: int =&gt; unit; };
*/

nat19.re

NatChurch.printUntil(3);
// x, f (x), f (f (x))

nat2.re

let zero: int = 0;
// let zero: int = 0;

let succ: int =&gt; int = x =&gt; x + 1;
// let succ: int =&gt; int = &lt;fun&gt;;

nat3.re

let zeroInt: natGroup(int) = zero =&gt; succ =&gt; zero;
// let zeroInt: natGroup(int) = &lt;fun&gt;;

let oneInt: natGroup(int) = zero =&gt; succ =&gt; succ (zero);
// let oneInt: natGroup(int) = &lt;fun&gt;;

let twoInt: natGroup(int) = zero =&gt; succ =&gt; succ (succ (zero));
// let twoInt: natGroup(int) = &lt;fun&gt;;

nat4.re

zeroInt(zero, succ); oneInt(zero, succ); twoInt(zero, succ);
// - : int = 0
// - : int = 1
// - : int = 2

nat5.re

module Nat = {
  type t = int;
  
  let zero: t = 0;
  let succ: t =&gt; t = x =&gt; x + 1;
}
// module Nat: { type t = int; let zero: t; let succ: t =&gt; t; };

nat6.re

Nat.(zero); Nat.(succ(zero)); Nat.(succ(succ(zero)));
// - : Nat.t = 0
// - : Nat.t = 1
// - : Nat.t = 2

nat7.re

module type NatGroup = {
  type t;
  
  let zero: t;
  let succ: t =&gt; t;
};
// module type NatGroup = { type t; let zero: t; let succ: t =&gt; t; };

nat8.re

module NatPriv: NatGroup = {
  include Nat; 
  let aPrivateMethod = () =&gt; (); // This stays within the module.
};
// module NatPriv: NatGroup;

nat9.re

module type ShowNatGroup = {
  include NatGroup;
  let toString: t =&gt; string;
}
/* 
module type ShowNatGroup =
  { type t; let zero: t; let succ: t =&gt; t; let toString: t =&gt; string; };
*/</code></pre><p>Now, generating numbers is just a matter of passing the module. Simple, right?</p><pre><code>nat.re

type natGroup(&#x27;t) = &#x27;t =&gt; (&#x27;t =&gt; &#x27;t) =&gt; &#x27;t;

---

let zero: int = 0;
let succ: int =&gt; int = x =&gt; x + 1;

---

let zeroInt: natGroup(int) = zero =&gt; succ =&gt; zero;
let oneInt: natGroup(int) = zero =&gt; succ =&gt; succ (zero);
let twoInt: natGroup(int) = zero =&gt; succ =&gt; succ (succ (zero));

--- 

zeroInt(zero, succ); oneInt(zero, succ); twoInt(zero, succ);

---

module Nat = {
  type t = int;
  
  let zero: t = 0;
  let succ: t =&gt; t = x =&gt; x + 1;
}

---

Nat.(zero); Nat.(succ(zero)); Nat.(succ(succ(zero)));

---

module type NatGroup = {
  type t;
  
  let zero: t;
  let succ: t =&gt; t;
};

---

module NatPriv: NatGroup = {
  include Nat; 
  let aPrivateMethod = () =&gt; (); // This stays within the module.
};

---

module type ShowNatGroup = {
  include NatGroup;
  let toString: t =&gt; string;
}

---

module ShowNat: ShowNatGroup = {
  include Nat;
  
  let toString = n =&gt; n == zero ? &quot;IsZero&quot; : &quot;IsNotZero&quot;; 
}

---

ShowNat.(zero); ShowNat.(succ(zero)); ShowNat.(succ(succ(zero)));

---

ShowNat.(toString(zero)); ShowNat.(toString(succ(zero)));

---

module type Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let printUntil: int =&gt; unit;
};

---

module Nat: Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let rec getItem = fun
    | 0 =&gt; ShowNatGroup.zero
    | i =&gt; ShowNatGroup.succ(getItem(i - 1));
  
  let printItem = item =&gt; print_endline(ShowNatGroup.toString(item));
  
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? ShowNatGroup.toString(item) : acc ++ &quot;, &quot; ++ ShowNatGroup.toString(item);
  
  let printUntil = n =&gt; {
    let items = List.init(n, getItem);
    print_endline(List.fold_left(join, &quot;&quot;, items));
  };
};

---

module NatInt = Nat({
  type t = int;
  let zero = 0;
  let succ = t =&gt; t + 1;
  let toString = string_of_int;
});

---

module NatBool = Nat({
  type t = bool;
  let zero = false;
  let succ = _ =&gt; true;
  let toString = string_of_bool;
});

---

module NatTern = Nat({
  type t = option(bool);
  let zero = Some(false);
  let succ = fun
    | Some(false) =&gt; None
    | _ =&gt; Some(true);
  let toString = fun
    | Some(item) =&gt; string_of_bool(item)
    | None =&gt; &quot;null&quot;;
});

---

NatBool.printUntil(3);
NatTern.printUntil(3);
NatInt.printUntil(3);

---

module NatChurch = {
  // Here&#x27;s where we get a bit creative with how we combine our Nats.
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? item : item ++ &quot; (&quot; ++ acc ++ &quot;)&quot;;

  // Extending the Nat functor for a specialized case. This is where ReasonML&#x27;s flexibility really shines.
  include Nat({
    type t = list(string);
    let zero = [];
    let succ = t =&gt; [&quot;f&quot;, ...t];
    let toString = t =&gt; List.fold_left(join, &quot;x&quot;, t);
  });
}

---

NatChurch.printUntil(3); 

nat1.re

type natGroup(&#x27;t) = &#x27;t =&gt; (&#x27;t =&gt; &#x27;t) =&gt; &#x27;t;
// type natGroup(&#x27;t) = (&#x27;t, &#x27;t =&gt; &#x27;t) =&gt; &#x27;t;

nat10.re

ShowNat.(zero); ShowNat.(succ(zero)); ShowNat.(succ(succ(zero)));
// - : ShowNat.t = &lt;abstr&gt;
// - : ShowNat.t = &lt;abstr&gt;
// - : ShowNat.t = &lt;abstr&gt;

nat10Real.re

module ShowNat: ShowNatGroup = {
  include Nat;
  
  let toString = n =&gt; n == zero ? &quot;IsZero&quot; : &quot;IsNotZero&quot;; 
}
// module ShowNat: ShowNatGroup;

nat11.re

ShowNat.(toString(zero)); ShowNat.(toString(succ(zero)));
// - : string = &quot;IsZero&quot;
// - : string = &quot;IsNotZero&quot;

nat12.re

module type Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let printUntil: int =&gt; unit;
};
/*
module type Nat =
  (ShowNatGroup : ShowNatGroup) =&gt; { let printUntil: int =&gt; unit; };
*/

nat13.re

module Nat: Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let rec getItem = fun
    | 0 =&gt; ShowNatGroup.zero
    | i =&gt; ShowNatGroup.succ(getItem(i - 1));
  
  let printItem = item =&gt; print_endline(ShowNatGroup.toString(item));
  
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? ShowNatGroup.toString(item) : acc ++ &quot;, &quot; ++ ShowNatGroup.toString(item);
  
  let printUntil = n =&gt; {
    let items = List.init(n, getItem);
    print_endline(List.fold_left(join, &quot;&quot;, items));
  };
};
// module Nat: Nat;

nat14.re

module NatInt = Nat({
  type t = int;
  let zero = 0;
  let succ = t =&gt; t + 1;
  let toString = string_of_int;
});
// module NatInt: { let printUntil: int =&gt; unit; };

nat15.re

module NatBool = Nat({
  type t = bool;
  let zero = false;
  let succ = _ =&gt; true;
  let toString = string_of_bool;
});
// module NatBool: { let printUntil: int =&gt; unit; };

nat16.re

module NatTern = Nat({
  type t = option(bool);
  let zero = Some(false);
  let succ = fun
    | Some(false) =&gt; None
    | _ =&gt; Some(true);
  let toString = fun
    | Some(item) =&gt; string_of_bool(item)
    | None =&gt; &quot;null&quot;;
});
// module NatTern: { let printUntil: int =&gt; unit; };

nat17.re

NatBool.printUntil(3);
// false, true, true

NatTern.printUntil(3);
// false, null, true

NatInt.printUntil(3);
// 0, 1, 2

nat18.re

module NatChurch = {
  // Here&#x27;s where we get a bit creative with how we combine our Nats.
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? item : item ++ &quot; (&quot; ++ acc ++ &quot;)&quot;;

  // Extending the Nat functor for a specialized case. This is where ReasonML&#x27;s flexibility really shines.
  include Nat({
    type t = list(string);
    let zero = [];
    let succ = t =&gt; [&quot;f&quot;, ...t];
    let toString = t =&gt; List.fold_left(join, &quot;x&quot;, t);
  });
}
/* 
module NatChurch:
  { let join: (string, string) =&gt; string; let printUntil: int =&gt; unit; };
*/

nat19.re

NatChurch.printUntil(3);
// x, f (x), f (f (x))

nat2.re

let zero: int = 0;
// let zero: int = 0;

let succ: int =&gt; int = x =&gt; x + 1;
// let succ: int =&gt; int = &lt;fun&gt;;

nat3.re

let zeroInt: natGroup(int) = zero =&gt; succ =&gt; zero;
// let zeroInt: natGroup(int) = &lt;fun&gt;;

let oneInt: natGroup(int) = zero =&gt; succ =&gt; succ (zero);
// let oneInt: natGroup(int) = &lt;fun&gt;;

let twoInt: natGroup(int) = zero =&gt; succ =&gt; succ (succ (zero));
// let twoInt: natGroup(int) = &lt;fun&gt;;

nat4.re

zeroInt(zero, succ); oneInt(zero, succ); twoInt(zero, succ);
// - : int = 0
// - : int = 1
// - : int = 2

nat5.re

module Nat = {
  type t = int;
  
  let zero: t = 0;
  let succ: t =&gt; t = x =&gt; x + 1;
}
// module Nat: { type t = int; let zero: t; let succ: t =&gt; t; };

nat6.re

Nat.(zero); Nat.(succ(zero)); Nat.(succ(succ(zero)));
// - : Nat.t = 0
// - : Nat.t = 1
// - : Nat.t = 2

nat7.re

module type NatGroup = {
  type t;
  
  let zero: t;
  let succ: t =&gt; t;
};
// module type NatGroup = { type t; let zero: t; let succ: t =&gt; t; };

nat8.re

module NatPriv: NatGroup = {
  include Nat; 
  let aPrivateMethod = () =&gt; (); // This stays within the module.
};
// module NatPriv: NatGroup;

nat9.re

module type ShowNatGroup = {
  include NatGroup;
  let toString: t =&gt; string;
}
/* 
module type ShowNatGroup =
  { type t; let zero: t; let succ: t =&gt; t; let toString: t =&gt; string; };
*/</code></pre><p>But exposing all functions, including the ones meant for internal use, could be an issue. That’s where interfaces come into play. Interfaces let you control what the user sees and uses, while implementations handle the functionality behind the scenes. Here’s what users should interact with:</p><pre><code>nat.re

type natGroup(&#x27;t) = &#x27;t =&gt; (&#x27;t =&gt; &#x27;t) =&gt; &#x27;t;

---

let zero: int = 0;
let succ: int =&gt; int = x =&gt; x + 1;

---

let zeroInt: natGroup(int) = zero =&gt; succ =&gt; zero;
let oneInt: natGroup(int) = zero =&gt; succ =&gt; succ (zero);
let twoInt: natGroup(int) = zero =&gt; succ =&gt; succ (succ (zero));

--- 

zeroInt(zero, succ); oneInt(zero, succ); twoInt(zero, succ);

---

module Nat = {
  type t = int;
  
  let zero: t = 0;
  let succ: t =&gt; t = x =&gt; x + 1;
}

---

Nat.(zero); Nat.(succ(zero)); Nat.(succ(succ(zero)));

---

module type NatGroup = {
  type t;
  
  let zero: t;
  let succ: t =&gt; t;
};

---

module NatPriv: NatGroup = {
  include Nat; 
  let aPrivateMethod = () =&gt; (); // This stays within the module.
};

---

module type ShowNatGroup = {
  include NatGroup;
  let toString: t =&gt; string;
}

---

module ShowNat: ShowNatGroup = {
  include Nat;
  
  let toString = n =&gt; n == zero ? &quot;IsZero&quot; : &quot;IsNotZero&quot;; 
}

---

ShowNat.(zero); ShowNat.(succ(zero)); ShowNat.(succ(succ(zero)));

---

ShowNat.(toString(zero)); ShowNat.(toString(succ(zero)));

---

module type Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let printUntil: int =&gt; unit;
};

---

module Nat: Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let rec getItem = fun
    | 0 =&gt; ShowNatGroup.zero
    | i =&gt; ShowNatGroup.succ(getItem(i - 1));
  
  let printItem = item =&gt; print_endline(ShowNatGroup.toString(item));
  
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? ShowNatGroup.toString(item) : acc ++ &quot;, &quot; ++ ShowNatGroup.toString(item);
  
  let printUntil = n =&gt; {
    let items = List.init(n, getItem);
    print_endline(List.fold_left(join, &quot;&quot;, items));
  };
};

---

module NatInt = Nat({
  type t = int;
  let zero = 0;
  let succ = t =&gt; t + 1;
  let toString = string_of_int;
});

---

module NatBool = Nat({
  type t = bool;
  let zero = false;
  let succ = _ =&gt; true;
  let toString = string_of_bool;
});

---

module NatTern = Nat({
  type t = option(bool);
  let zero = Some(false);
  let succ = fun
    | Some(false) =&gt; None
    | _ =&gt; Some(true);
  let toString = fun
    | Some(item) =&gt; string_of_bool(item)
    | None =&gt; &quot;null&quot;;
});

---

NatBool.printUntil(3);
NatTern.printUntil(3);
NatInt.printUntil(3);

---

module NatChurch = {
  // Here&#x27;s where we get a bit creative with how we combine our Nats.
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? item : item ++ &quot; (&quot; ++ acc ++ &quot;)&quot;;

  // Extending the Nat functor for a specialized case. This is where ReasonML&#x27;s flexibility really shines.
  include Nat({
    type t = list(string);
    let zero = [];
    let succ = t =&gt; [&quot;f&quot;, ...t];
    let toString = t =&gt; List.fold_left(join, &quot;x&quot;, t);
  });
}

---

NatChurch.printUntil(3); 

nat1.re

type natGroup(&#x27;t) = &#x27;t =&gt; (&#x27;t =&gt; &#x27;t) =&gt; &#x27;t;
// type natGroup(&#x27;t) = (&#x27;t, &#x27;t =&gt; &#x27;t) =&gt; &#x27;t;

nat10.re

ShowNat.(zero); ShowNat.(succ(zero)); ShowNat.(succ(succ(zero)));
// - : ShowNat.t = &lt;abstr&gt;
// - : ShowNat.t = &lt;abstr&gt;
// - : ShowNat.t = &lt;abstr&gt;

nat10Real.re

module ShowNat: ShowNatGroup = {
  include Nat;
  
  let toString = n =&gt; n == zero ? &quot;IsZero&quot; : &quot;IsNotZero&quot;; 
}
// module ShowNat: ShowNatGroup;

nat11.re

ShowNat.(toString(zero)); ShowNat.(toString(succ(zero)));
// - : string = &quot;IsZero&quot;
// - : string = &quot;IsNotZero&quot;

nat12.re

module type Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let printUntil: int =&gt; unit;
};
/*
module type Nat =
  (ShowNatGroup : ShowNatGroup) =&gt; { let printUntil: int =&gt; unit; };
*/

nat13.re

module Nat: Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let rec getItem = fun
    | 0 =&gt; ShowNatGroup.zero
    | i =&gt; ShowNatGroup.succ(getItem(i - 1));
  
  let printItem = item =&gt; print_endline(ShowNatGroup.toString(item));
  
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? ShowNatGroup.toString(item) : acc ++ &quot;, &quot; ++ ShowNatGroup.toString(item);
  
  let printUntil = n =&gt; {
    let items = List.init(n, getItem);
    print_endline(List.fold_left(join, &quot;&quot;, items));
  };
};
// module Nat: Nat;

nat14.re

module NatInt = Nat({
  type t = int;
  let zero = 0;
  let succ = t =&gt; t + 1;
  let toString = string_of_int;
});
// module NatInt: { let printUntil: int =&gt; unit; };

nat15.re

module NatBool = Nat({
  type t = bool;
  let zero = false;
  let succ = _ =&gt; true;
  let toString = string_of_bool;
});
// module NatBool: { let printUntil: int =&gt; unit; };

nat16.re

module NatTern = Nat({
  type t = option(bool);
  let zero = Some(false);
  let succ = fun
    | Some(false) =&gt; None
    | _ =&gt; Some(true);
  let toString = fun
    | Some(item) =&gt; string_of_bool(item)
    | None =&gt; &quot;null&quot;;
});
// module NatTern: { let printUntil: int =&gt; unit; };

nat17.re

NatBool.printUntil(3);
// false, true, true

NatTern.printUntil(3);
// false, null, true

NatInt.printUntil(3);
// 0, 1, 2

nat18.re

module NatChurch = {
  // Here&#x27;s where we get a bit creative with how we combine our Nats.
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? item : item ++ &quot; (&quot; ++ acc ++ &quot;)&quot;;

  // Extending the Nat functor for a specialized case. This is where ReasonML&#x27;s flexibility really shines.
  include Nat({
    type t = list(string);
    let zero = [];
    let succ = t =&gt; [&quot;f&quot;, ...t];
    let toString = t =&gt; List.fold_left(join, &quot;x&quot;, t);
  });
}
/* 
module NatChurch:
  { let join: (string, string) =&gt; string; let printUntil: int =&gt; unit; };
*/

nat19.re

NatChurch.printUntil(3);
// x, f (x), f (f (x))

nat2.re

let zero: int = 0;
// let zero: int = 0;

let succ: int =&gt; int = x =&gt; x + 1;
// let succ: int =&gt; int = &lt;fun&gt;;

nat3.re

let zeroInt: natGroup(int) = zero =&gt; succ =&gt; zero;
// let zeroInt: natGroup(int) = &lt;fun&gt;;

let oneInt: natGroup(int) = zero =&gt; succ =&gt; succ (zero);
// let oneInt: natGroup(int) = &lt;fun&gt;;

let twoInt: natGroup(int) = zero =&gt; succ =&gt; succ (succ (zero));
// let twoInt: natGroup(int) = &lt;fun&gt;;

nat4.re

zeroInt(zero, succ); oneInt(zero, succ); twoInt(zero, succ);
// - : int = 0
// - : int = 1
// - : int = 2

nat5.re

module Nat = {
  type t = int;
  
  let zero: t = 0;
  let succ: t =&gt; t = x =&gt; x + 1;
}
// module Nat: { type t = int; let zero: t; let succ: t =&gt; t; };

nat6.re

Nat.(zero); Nat.(succ(zero)); Nat.(succ(succ(zero)));
// - : Nat.t = 0
// - : Nat.t = 1
// - : Nat.t = 2

nat7.re

module type NatGroup = {
  type t;
  
  let zero: t;
  let succ: t =&gt; t;
};
// module type NatGroup = { type t; let zero: t; let succ: t =&gt; t; };

nat8.re

module NatPriv: NatGroup = {
  include Nat; 
  let aPrivateMethod = () =&gt; (); // This stays within the module.
};
// module NatPriv: NatGroup;

nat9.re

module type ShowNatGroup = {
  include NatGroup;
  let toString: t =&gt; string;
}
/* 
module type ShowNatGroup =
  { type t; let zero: t; let succ: t =&gt; t; let toString: t =&gt; string; };
*/</code></pre><p>Inheriting without repetition is key. If NatPriv doesn’t show a method, it’s because NatGroup didn’t list it.</p><pre><code>nat.re

type natGroup(&#x27;t) = &#x27;t =&gt; (&#x27;t =&gt; &#x27;t) =&gt; &#x27;t;

---

let zero: int = 0;
let succ: int =&gt; int = x =&gt; x + 1;

---

let zeroInt: natGroup(int) = zero =&gt; succ =&gt; zero;
let oneInt: natGroup(int) = zero =&gt; succ =&gt; succ (zero);
let twoInt: natGroup(int) = zero =&gt; succ =&gt; succ (succ (zero));

--- 

zeroInt(zero, succ); oneInt(zero, succ); twoInt(zero, succ);

---

module Nat = {
  type t = int;
  
  let zero: t = 0;
  let succ: t =&gt; t = x =&gt; x + 1;
}

---

Nat.(zero); Nat.(succ(zero)); Nat.(succ(succ(zero)));

---

module type NatGroup = {
  type t;
  
  let zero: t;
  let succ: t =&gt; t;
};

---

module NatPriv: NatGroup = {
  include Nat; 
  let aPrivateMethod = () =&gt; (); // This stays within the module.
};

---

module type ShowNatGroup = {
  include NatGroup;
  let toString: t =&gt; string;
}

---

module ShowNat: ShowNatGroup = {
  include Nat;
  
  let toString = n =&gt; n == zero ? &quot;IsZero&quot; : &quot;IsNotZero&quot;; 
}

---

ShowNat.(zero); ShowNat.(succ(zero)); ShowNat.(succ(succ(zero)));

---

ShowNat.(toString(zero)); ShowNat.(toString(succ(zero)));

---

module type Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let printUntil: int =&gt; unit;
};

---

module Nat: Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let rec getItem = fun
    | 0 =&gt; ShowNatGroup.zero
    | i =&gt; ShowNatGroup.succ(getItem(i - 1));
  
  let printItem = item =&gt; print_endline(ShowNatGroup.toString(item));
  
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? ShowNatGroup.toString(item) : acc ++ &quot;, &quot; ++ ShowNatGroup.toString(item);
  
  let printUntil = n =&gt; {
    let items = List.init(n, getItem);
    print_endline(List.fold_left(join, &quot;&quot;, items));
  };
};

---

module NatInt = Nat({
  type t = int;
  let zero = 0;
  let succ = t =&gt; t + 1;
  let toString = string_of_int;
});

---

module NatBool = Nat({
  type t = bool;
  let zero = false;
  let succ = _ =&gt; true;
  let toString = string_of_bool;
});

---

module NatTern = Nat({
  type t = option(bool);
  let zero = Some(false);
  let succ = fun
    | Some(false) =&gt; None
    | _ =&gt; Some(true);
  let toString = fun
    | Some(item) =&gt; string_of_bool(item)
    | None =&gt; &quot;null&quot;;
});

---

NatBool.printUntil(3);
NatTern.printUntil(3);
NatInt.printUntil(3);

---

module NatChurch = {
  // Here&#x27;s where we get a bit creative with how we combine our Nats.
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? item : item ++ &quot; (&quot; ++ acc ++ &quot;)&quot;;

  // Extending the Nat functor for a specialized case. This is where ReasonML&#x27;s flexibility really shines.
  include Nat({
    type t = list(string);
    let zero = [];
    let succ = t =&gt; [&quot;f&quot;, ...t];
    let toString = t =&gt; List.fold_left(join, &quot;x&quot;, t);
  });
}

---

NatChurch.printUntil(3); 

nat1.re

type natGroup(&#x27;t) = &#x27;t =&gt; (&#x27;t =&gt; &#x27;t) =&gt; &#x27;t;
// type natGroup(&#x27;t) = (&#x27;t, &#x27;t =&gt; &#x27;t) =&gt; &#x27;t;

nat10.re

ShowNat.(zero); ShowNat.(succ(zero)); ShowNat.(succ(succ(zero)));
// - : ShowNat.t = &lt;abstr&gt;
// - : ShowNat.t = &lt;abstr&gt;
// - : ShowNat.t = &lt;abstr&gt;

nat10Real.re

module ShowNat: ShowNatGroup = {
  include Nat;
  
  let toString = n =&gt; n == zero ? &quot;IsZero&quot; : &quot;IsNotZero&quot;; 
}
// module ShowNat: ShowNatGroup;

nat11.re

ShowNat.(toString(zero)); ShowNat.(toString(succ(zero)));
// - : string = &quot;IsZero&quot;
// - : string = &quot;IsNotZero&quot;

nat12.re

module type Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let printUntil: int =&gt; unit;
};
/*
module type Nat =
  (ShowNatGroup : ShowNatGroup) =&gt; { let printUntil: int =&gt; unit; };
*/

nat13.re

module Nat: Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let rec getItem = fun
    | 0 =&gt; ShowNatGroup.zero
    | i =&gt; ShowNatGroup.succ(getItem(i - 1));
  
  let printItem = item =&gt; print_endline(ShowNatGroup.toString(item));
  
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? ShowNatGroup.toString(item) : acc ++ &quot;, &quot; ++ ShowNatGroup.toString(item);
  
  let printUntil = n =&gt; {
    let items = List.init(n, getItem);
    print_endline(List.fold_left(join, &quot;&quot;, items));
  };
};
// module Nat: Nat;

nat14.re

module NatInt = Nat({
  type t = int;
  let zero = 0;
  let succ = t =&gt; t + 1;
  let toString = string_of_int;
});
// module NatInt: { let printUntil: int =&gt; unit; };

nat15.re

module NatBool = Nat({
  type t = bool;
  let zero = false;
  let succ = _ =&gt; true;
  let toString = string_of_bool;
});
// module NatBool: { let printUntil: int =&gt; unit; };

nat16.re

module NatTern = Nat({
  type t = option(bool);
  let zero = Some(false);
  let succ = fun
    | Some(false) =&gt; None
    | _ =&gt; Some(true);
  let toString = fun
    | Some(item) =&gt; string_of_bool(item)
    | None =&gt; &quot;null&quot;;
});
// module NatTern: { let printUntil: int =&gt; unit; };

nat17.re

NatBool.printUntil(3);
// false, true, true

NatTern.printUntil(3);
// false, null, true

NatInt.printUntil(3);
// 0, 1, 2

nat18.re

module NatChurch = {
  // Here&#x27;s where we get a bit creative with how we combine our Nats.
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? item : item ++ &quot; (&quot; ++ acc ++ &quot;)&quot;;

  // Extending the Nat functor for a specialized case. This is where ReasonML&#x27;s flexibility really shines.
  include Nat({
    type t = list(string);
    let zero = [];
    let succ = t =&gt; [&quot;f&quot;, ...t];
    let toString = t =&gt; List.fold_left(join, &quot;x&quot;, t);
  });
}
/* 
module NatChurch:
  { let join: (string, string) =&gt; string; let printUntil: int =&gt; unit; };
*/

nat19.re

NatChurch.printUntil(3);
// x, f (x), f (f (x))

nat2.re

let zero: int = 0;
// let zero: int = 0;

let succ: int =&gt; int = x =&gt; x + 1;
// let succ: int =&gt; int = &lt;fun&gt;;

nat3.re

let zeroInt: natGroup(int) = zero =&gt; succ =&gt; zero;
// let zeroInt: natGroup(int) = &lt;fun&gt;;

let oneInt: natGroup(int) = zero =&gt; succ =&gt; succ (zero);
// let oneInt: natGroup(int) = &lt;fun&gt;;

let twoInt: natGroup(int) = zero =&gt; succ =&gt; succ (succ (zero));
// let twoInt: natGroup(int) = &lt;fun&gt;;

nat4.re

zeroInt(zero, succ); oneInt(zero, succ); twoInt(zero, succ);
// - : int = 0
// - : int = 1
// - : int = 2

nat5.re

module Nat = {
  type t = int;
  
  let zero: t = 0;
  let succ: t =&gt; t = x =&gt; x + 1;
}
// module Nat: { type t = int; let zero: t; let succ: t =&gt; t; };

nat6.re

Nat.(zero); Nat.(succ(zero)); Nat.(succ(succ(zero)));
// - : Nat.t = 0
// - : Nat.t = 1
// - : Nat.t = 2

nat7.re

module type NatGroup = {
  type t;
  
  let zero: t;
  let succ: t =&gt; t;
};
// module type NatGroup = { type t; let zero: t; let succ: t =&gt; t; };

nat8.re

module NatPriv: NatGroup = {
  include Nat; 
  let aPrivateMethod = () =&gt; (); // This stays within the module.
};
// module NatPriv: NatGroup;

nat9.re

module type ShowNatGroup = {
  include NatGroup;
  let toString: t =&gt; string;
}
/* 
module type ShowNatGroup =
  { type t; let zero: t; let succ: t =&gt; t; let toString: t =&gt; string; };
*/</code></pre><p>Extending interfaces allows for additional methods without redundancy.</p><pre><code>nat.re

type natGroup(&#x27;t) = &#x27;t =&gt; (&#x27;t =&gt; &#x27;t) =&gt; &#x27;t;

---

let zero: int = 0;
let succ: int =&gt; int = x =&gt; x + 1;

---

let zeroInt: natGroup(int) = zero =&gt; succ =&gt; zero;
let oneInt: natGroup(int) = zero =&gt; succ =&gt; succ (zero);
let twoInt: natGroup(int) = zero =&gt; succ =&gt; succ (succ (zero));

--- 

zeroInt(zero, succ); oneInt(zero, succ); twoInt(zero, succ);

---

module Nat = {
  type t = int;
  
  let zero: t = 0;
  let succ: t =&gt; t = x =&gt; x + 1;
}

---

Nat.(zero); Nat.(succ(zero)); Nat.(succ(succ(zero)));

---

module type NatGroup = {
  type t;
  
  let zero: t;
  let succ: t =&gt; t;
};

---

module NatPriv: NatGroup = {
  include Nat; 
  let aPrivateMethod = () =&gt; (); // This stays within the module.
};

---

module type ShowNatGroup = {
  include NatGroup;
  let toString: t =&gt; string;
}

---

module ShowNat: ShowNatGroup = {
  include Nat;
  
  let toString = n =&gt; n == zero ? &quot;IsZero&quot; : &quot;IsNotZero&quot;; 
}

---

ShowNat.(zero); ShowNat.(succ(zero)); ShowNat.(succ(succ(zero)));

---

ShowNat.(toString(zero)); ShowNat.(toString(succ(zero)));

---

module type Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let printUntil: int =&gt; unit;
};

---

module Nat: Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let rec getItem = fun
    | 0 =&gt; ShowNatGroup.zero
    | i =&gt; ShowNatGroup.succ(getItem(i - 1));
  
  let printItem = item =&gt; print_endline(ShowNatGroup.toString(item));
  
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? ShowNatGroup.toString(item) : acc ++ &quot;, &quot; ++ ShowNatGroup.toString(item);
  
  let printUntil = n =&gt; {
    let items = List.init(n, getItem);
    print_endline(List.fold_left(join, &quot;&quot;, items));
  };
};

---

module NatInt = Nat({
  type t = int;
  let zero = 0;
  let succ = t =&gt; t + 1;
  let toString = string_of_int;
});

---

module NatBool = Nat({
  type t = bool;
  let zero = false;
  let succ = _ =&gt; true;
  let toString = string_of_bool;
});

---

module NatTern = Nat({
  type t = option(bool);
  let zero = Some(false);
  let succ = fun
    | Some(false) =&gt; None
    | _ =&gt; Some(true);
  let toString = fun
    | Some(item) =&gt; string_of_bool(item)
    | None =&gt; &quot;null&quot;;
});

---

NatBool.printUntil(3);
NatTern.printUntil(3);
NatInt.printUntil(3);

---

module NatChurch = {
  // Here&#x27;s where we get a bit creative with how we combine our Nats.
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? item : item ++ &quot; (&quot; ++ acc ++ &quot;)&quot;;

  // Extending the Nat functor for a specialized case. This is where ReasonML&#x27;s flexibility really shines.
  include Nat({
    type t = list(string);
    let zero = [];
    let succ = t =&gt; [&quot;f&quot;, ...t];
    let toString = t =&gt; List.fold_left(join, &quot;x&quot;, t);
  });
}

---

NatChurch.printUntil(3); 

nat1.re

type natGroup(&#x27;t) = &#x27;t =&gt; (&#x27;t =&gt; &#x27;t) =&gt; &#x27;t;
// type natGroup(&#x27;t) = (&#x27;t, &#x27;t =&gt; &#x27;t) =&gt; &#x27;t;

nat10.re

ShowNat.(zero); ShowNat.(succ(zero)); ShowNat.(succ(succ(zero)));
// - : ShowNat.t = &lt;abstr&gt;
// - : ShowNat.t = &lt;abstr&gt;
// - : ShowNat.t = &lt;abstr&gt;

nat10Real.re

module ShowNat: ShowNatGroup = {
  include Nat;
  
  let toString = n =&gt; n == zero ? &quot;IsZero&quot; : &quot;IsNotZero&quot;; 
}
// module ShowNat: ShowNatGroup;

nat11.re

ShowNat.(toString(zero)); ShowNat.(toString(succ(zero)));
// - : string = &quot;IsZero&quot;
// - : string = &quot;IsNotZero&quot;

nat12.re

module type Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let printUntil: int =&gt; unit;
};
/*
module type Nat =
  (ShowNatGroup : ShowNatGroup) =&gt; { let printUntil: int =&gt; unit; };
*/

nat13.re

module Nat: Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let rec getItem = fun
    | 0 =&gt; ShowNatGroup.zero
    | i =&gt; ShowNatGroup.succ(getItem(i - 1));
  
  let printItem = item =&gt; print_endline(ShowNatGroup.toString(item));
  
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? ShowNatGroup.toString(item) : acc ++ &quot;, &quot; ++ ShowNatGroup.toString(item);
  
  let printUntil = n =&gt; {
    let items = List.init(n, getItem);
    print_endline(List.fold_left(join, &quot;&quot;, items));
  };
};
// module Nat: Nat;

nat14.re

module NatInt = Nat({
  type t = int;
  let zero = 0;
  let succ = t =&gt; t + 1;
  let toString = string_of_int;
});
// module NatInt: { let printUntil: int =&gt; unit; };

nat15.re

module NatBool = Nat({
  type t = bool;
  let zero = false;
  let succ = _ =&gt; true;
  let toString = string_of_bool;
});
// module NatBool: { let printUntil: int =&gt; unit; };

nat16.re

module NatTern = Nat({
  type t = option(bool);
  let zero = Some(false);
  let succ = fun
    | Some(false) =&gt; None
    | _ =&gt; Some(true);
  let toString = fun
    | Some(item) =&gt; string_of_bool(item)
    | None =&gt; &quot;null&quot;;
});
// module NatTern: { let printUntil: int =&gt; unit; };

nat17.re

NatBool.printUntil(3);
// false, true, true

NatTern.printUntil(3);
// false, null, true

NatInt.printUntil(3);
// 0, 1, 2

nat18.re

module NatChurch = {
  // Here&#x27;s where we get a bit creative with how we combine our Nats.
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? item : item ++ &quot; (&quot; ++ acc ++ &quot;)&quot;;

  // Extending the Nat functor for a specialized case. This is where ReasonML&#x27;s flexibility really shines.
  include Nat({
    type t = list(string);
    let zero = [];
    let succ = t =&gt; [&quot;f&quot;, ...t];
    let toString = t =&gt; List.fold_left(join, &quot;x&quot;, t);
  });
}
/* 
module NatChurch:
  { let join: (string, string) =&gt; string; let printUntil: int =&gt; unit; };
*/

nat19.re

NatChurch.printUntil(3);
// x, f (x), f (f (x))

nat2.re

let zero: int = 0;
// let zero: int = 0;

let succ: int =&gt; int = x =&gt; x + 1;
// let succ: int =&gt; int = &lt;fun&gt;;

nat3.re

let zeroInt: natGroup(int) = zero =&gt; succ =&gt; zero;
// let zeroInt: natGroup(int) = &lt;fun&gt;;

let oneInt: natGroup(int) = zero =&gt; succ =&gt; succ (zero);
// let oneInt: natGroup(int) = &lt;fun&gt;;

let twoInt: natGroup(int) = zero =&gt; succ =&gt; succ (succ (zero));
// let twoInt: natGroup(int) = &lt;fun&gt;;

nat4.re

zeroInt(zero, succ); oneInt(zero, succ); twoInt(zero, succ);
// - : int = 0
// - : int = 1
// - : int = 2

nat5.re

module Nat = {
  type t = int;
  
  let zero: t = 0;
  let succ: t =&gt; t = x =&gt; x + 1;
}
// module Nat: { type t = int; let zero: t; let succ: t =&gt; t; };

nat6.re

Nat.(zero); Nat.(succ(zero)); Nat.(succ(succ(zero)));
// - : Nat.t = 0
// - : Nat.t = 1
// - : Nat.t = 2

nat7.re

module type NatGroup = {
  type t;
  
  let zero: t;
  let succ: t =&gt; t;
};
// module type NatGroup = { type t; let zero: t; let succ: t =&gt; t; };

nat8.re

module NatPriv: NatGroup = {
  include Nat; 
  let aPrivateMethod = () =&gt; (); // This stays within the module.
};
// module NatPriv: NatGroup;

nat9.re

module type ShowNatGroup = {
  include NatGroup;
  let toString: t =&gt; string;
}
/* 
module type ShowNatGroup =
  { type t; let zero: t; let succ: t =&gt; t; let toString: t =&gt; string; };
*/</code></pre><p>Implementing ShowNat by including Nat and adding a toString method.</p><pre><code>nat.re

type natGroup(&#x27;t) = &#x27;t =&gt; (&#x27;t =&gt; &#x27;t) =&gt; &#x27;t;

---

let zero: int = 0;
let succ: int =&gt; int = x =&gt; x + 1;

---

let zeroInt: natGroup(int) = zero =&gt; succ =&gt; zero;
let oneInt: natGroup(int) = zero =&gt; succ =&gt; succ (zero);
let twoInt: natGroup(int) = zero =&gt; succ =&gt; succ (succ (zero));

--- 

zeroInt(zero, succ); oneInt(zero, succ); twoInt(zero, succ);

---

module Nat = {
  type t = int;
  
  let zero: t = 0;
  let succ: t =&gt; t = x =&gt; x + 1;
}

---

Nat.(zero); Nat.(succ(zero)); Nat.(succ(succ(zero)));

---

module type NatGroup = {
  type t;
  
  let zero: t;
  let succ: t =&gt; t;
};

---

module NatPriv: NatGroup = {
  include Nat; 
  let aPrivateMethod = () =&gt; (); // This stays within the module.
};

---

module type ShowNatGroup = {
  include NatGroup;
  let toString: t =&gt; string;
}

---

module ShowNat: ShowNatGroup = {
  include Nat;
  
  let toString = n =&gt; n == zero ? &quot;IsZero&quot; : &quot;IsNotZero&quot;; 
}

---

ShowNat.(zero); ShowNat.(succ(zero)); ShowNat.(succ(succ(zero)));

---

ShowNat.(toString(zero)); ShowNat.(toString(succ(zero)));

---

module type Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let printUntil: int =&gt; unit;
};

---

module Nat: Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let rec getItem = fun
    | 0 =&gt; ShowNatGroup.zero
    | i =&gt; ShowNatGroup.succ(getItem(i - 1));
  
  let printItem = item =&gt; print_endline(ShowNatGroup.toString(item));
  
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? ShowNatGroup.toString(item) : acc ++ &quot;, &quot; ++ ShowNatGroup.toString(item);
  
  let printUntil = n =&gt; {
    let items = List.init(n, getItem);
    print_endline(List.fold_left(join, &quot;&quot;, items));
  };
};

---

module NatInt = Nat({
  type t = int;
  let zero = 0;
  let succ = t =&gt; t + 1;
  let toString = string_of_int;
});

---

module NatBool = Nat({
  type t = bool;
  let zero = false;
  let succ = _ =&gt; true;
  let toString = string_of_bool;
});

---

module NatTern = Nat({
  type t = option(bool);
  let zero = Some(false);
  let succ = fun
    | Some(false) =&gt; None
    | _ =&gt; Some(true);
  let toString = fun
    | Some(item) =&gt; string_of_bool(item)
    | None =&gt; &quot;null&quot;;
});

---

NatBool.printUntil(3);
NatTern.printUntil(3);
NatInt.printUntil(3);

---

module NatChurch = {
  // Here&#x27;s where we get a bit creative with how we combine our Nats.
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? item : item ++ &quot; (&quot; ++ acc ++ &quot;)&quot;;

  // Extending the Nat functor for a specialized case. This is where ReasonML&#x27;s flexibility really shines.
  include Nat({
    type t = list(string);
    let zero = [];
    let succ = t =&gt; [&quot;f&quot;, ...t];
    let toString = t =&gt; List.fold_left(join, &quot;x&quot;, t);
  });
}

---

NatChurch.printUntil(3); 

nat1.re

type natGroup(&#x27;t) = &#x27;t =&gt; (&#x27;t =&gt; &#x27;t) =&gt; &#x27;t;
// type natGroup(&#x27;t) = (&#x27;t, &#x27;t =&gt; &#x27;t) =&gt; &#x27;t;

nat10.re

ShowNat.(zero); ShowNat.(succ(zero)); ShowNat.(succ(succ(zero)));
// - : ShowNat.t = &lt;abstr&gt;
// - : ShowNat.t = &lt;abstr&gt;
// - : ShowNat.t = &lt;abstr&gt;

nat10Real.re

module ShowNat: ShowNatGroup = {
  include Nat;
  
  let toString = n =&gt; n == zero ? &quot;IsZero&quot; : &quot;IsNotZero&quot;; 
}
// module ShowNat: ShowNatGroup;

nat11.re

ShowNat.(toString(zero)); ShowNat.(toString(succ(zero)));
// - : string = &quot;IsZero&quot;
// - : string = &quot;IsNotZero&quot;

nat12.re

module type Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let printUntil: int =&gt; unit;
};
/*
module type Nat =
  (ShowNatGroup : ShowNatGroup) =&gt; { let printUntil: int =&gt; unit; };
*/

nat13.re

module Nat: Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let rec getItem = fun
    | 0 =&gt; ShowNatGroup.zero
    | i =&gt; ShowNatGroup.succ(getItem(i - 1));
  
  let printItem = item =&gt; print_endline(ShowNatGroup.toString(item));
  
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? ShowNatGroup.toString(item) : acc ++ &quot;, &quot; ++ ShowNatGroup.toString(item);
  
  let printUntil = n =&gt; {
    let items = List.init(n, getItem);
    print_endline(List.fold_left(join, &quot;&quot;, items));
  };
};
// module Nat: Nat;

nat14.re

module NatInt = Nat({
  type t = int;
  let zero = 0;
  let succ = t =&gt; t + 1;
  let toString = string_of_int;
});
// module NatInt: { let printUntil: int =&gt; unit; };

nat15.re

module NatBool = Nat({
  type t = bool;
  let zero = false;
  let succ = _ =&gt; true;
  let toString = string_of_bool;
});
// module NatBool: { let printUntil: int =&gt; unit; };

nat16.re

module NatTern = Nat({
  type t = option(bool);
  let zero = Some(false);
  let succ = fun
    | Some(false) =&gt; None
    | _ =&gt; Some(true);
  let toString = fun
    | Some(item) =&gt; string_of_bool(item)
    | None =&gt; &quot;null&quot;;
});
// module NatTern: { let printUntil: int =&gt; unit; };

nat17.re

NatBool.printUntil(3);
// false, true, true

NatTern.printUntil(3);
// false, null, true

NatInt.printUntil(3);
// 0, 1, 2

nat18.re

module NatChurch = {
  // Here&#x27;s where we get a bit creative with how we combine our Nats.
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? item : item ++ &quot; (&quot; ++ acc ++ &quot;)&quot;;

  // Extending the Nat functor for a specialized case. This is where ReasonML&#x27;s flexibility really shines.
  include Nat({
    type t = list(string);
    let zero = [];
    let succ = t =&gt; [&quot;f&quot;, ...t];
    let toString = t =&gt; List.fold_left(join, &quot;x&quot;, t);
  });
}
/* 
module NatChurch:
  { let join: (string, string) =&gt; string; let printUntil: int =&gt; unit; };
*/

nat19.re

NatChurch.printUntil(3);
// x, f (x), f (f (x))

nat2.re

let zero: int = 0;
// let zero: int = 0;

let succ: int =&gt; int = x =&gt; x + 1;
// let succ: int =&gt; int = &lt;fun&gt;;

nat3.re

let zeroInt: natGroup(int) = zero =&gt; succ =&gt; zero;
// let zeroInt: natGroup(int) = &lt;fun&gt;;

let oneInt: natGroup(int) = zero =&gt; succ =&gt; succ (zero);
// let oneInt: natGroup(int) = &lt;fun&gt;;

let twoInt: natGroup(int) = zero =&gt; succ =&gt; succ (succ (zero));
// let twoInt: natGroup(int) = &lt;fun&gt;;

nat4.re

zeroInt(zero, succ); oneInt(zero, succ); twoInt(zero, succ);
// - : int = 0
// - : int = 1
// - : int = 2

nat5.re

module Nat = {
  type t = int;
  
  let zero: t = 0;
  let succ: t =&gt; t = x =&gt; x + 1;
}
// module Nat: { type t = int; let zero: t; let succ: t =&gt; t; };

nat6.re

Nat.(zero); Nat.(succ(zero)); Nat.(succ(succ(zero)));
// - : Nat.t = 0
// - : Nat.t = 1
// - : Nat.t = 2

nat7.re

module type NatGroup = {
  type t;
  
  let zero: t;
  let succ: t =&gt; t;
};
// module type NatGroup = { type t; let zero: t; let succ: t =&gt; t; };

nat8.re

module NatPriv: NatGroup = {
  include Nat; 
  let aPrivateMethod = () =&gt; (); // This stays within the module.
};
// module NatPriv: NatGroup;

nat9.re

module type ShowNatGroup = {
  include NatGroup;
  let toString: t =&gt; string;
}
/* 
module type ShowNatGroup =
  { type t; let zero: t; let succ: t =&gt; t; let toString: t =&gt; string; };
*/</code></pre><p>With interfaces, direct access to values is restricted, enhancing encapsulation.</p><pre><code>nat.re

type natGroup(&#x27;t) = &#x27;t =&gt; (&#x27;t =&gt; &#x27;t) =&gt; &#x27;t;

---

let zero: int = 0;
let succ: int =&gt; int = x =&gt; x + 1;

---

let zeroInt: natGroup(int) = zero =&gt; succ =&gt; zero;
let oneInt: natGroup(int) = zero =&gt; succ =&gt; succ (zero);
let twoInt: natGroup(int) = zero =&gt; succ =&gt; succ (succ (zero));

--- 

zeroInt(zero, succ); oneInt(zero, succ); twoInt(zero, succ);

---

module Nat = {
  type t = int;
  
  let zero: t = 0;
  let succ: t =&gt; t = x =&gt; x + 1;
}

---

Nat.(zero); Nat.(succ(zero)); Nat.(succ(succ(zero)));

---

module type NatGroup = {
  type t;
  
  let zero: t;
  let succ: t =&gt; t;
};

---

module NatPriv: NatGroup = {
  include Nat; 
  let aPrivateMethod = () =&gt; (); // This stays within the module.
};

---

module type ShowNatGroup = {
  include NatGroup;
  let toString: t =&gt; string;
}

---

module ShowNat: ShowNatGroup = {
  include Nat;
  
  let toString = n =&gt; n == zero ? &quot;IsZero&quot; : &quot;IsNotZero&quot;; 
}

---

ShowNat.(zero); ShowNat.(succ(zero)); ShowNat.(succ(succ(zero)));

---

ShowNat.(toString(zero)); ShowNat.(toString(succ(zero)));

---

module type Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let printUntil: int =&gt; unit;
};

---

module Nat: Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let rec getItem = fun
    | 0 =&gt; ShowNatGroup.zero
    | i =&gt; ShowNatGroup.succ(getItem(i - 1));
  
  let printItem = item =&gt; print_endline(ShowNatGroup.toString(item));
  
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? ShowNatGroup.toString(item) : acc ++ &quot;, &quot; ++ ShowNatGroup.toString(item);
  
  let printUntil = n =&gt; {
    let items = List.init(n, getItem);
    print_endline(List.fold_left(join, &quot;&quot;, items));
  };
};

---

module NatInt = Nat({
  type t = int;
  let zero = 0;
  let succ = t =&gt; t + 1;
  let toString = string_of_int;
});

---

module NatBool = Nat({
  type t = bool;
  let zero = false;
  let succ = _ =&gt; true;
  let toString = string_of_bool;
});

---

module NatTern = Nat({
  type t = option(bool);
  let zero = Some(false);
  let succ = fun
    | Some(false) =&gt; None
    | _ =&gt; Some(true);
  let toString = fun
    | Some(item) =&gt; string_of_bool(item)
    | None =&gt; &quot;null&quot;;
});

---

NatBool.printUntil(3);
NatTern.printUntil(3);
NatInt.printUntil(3);

---

module NatChurch = {
  // Here&#x27;s where we get a bit creative with how we combine our Nats.
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? item : item ++ &quot; (&quot; ++ acc ++ &quot;)&quot;;

  // Extending the Nat functor for a specialized case. This is where ReasonML&#x27;s flexibility really shines.
  include Nat({
    type t = list(string);
    let zero = [];
    let succ = t =&gt; [&quot;f&quot;, ...t];
    let toString = t =&gt; List.fold_left(join, &quot;x&quot;, t);
  });
}

---

NatChurch.printUntil(3); 

nat1.re

type natGroup(&#x27;t) = &#x27;t =&gt; (&#x27;t =&gt; &#x27;t) =&gt; &#x27;t;
// type natGroup(&#x27;t) = (&#x27;t, &#x27;t =&gt; &#x27;t) =&gt; &#x27;t;

nat10.re

ShowNat.(zero); ShowNat.(succ(zero)); ShowNat.(succ(succ(zero)));
// - : ShowNat.t = &lt;abstr&gt;
// - : ShowNat.t = &lt;abstr&gt;
// - : ShowNat.t = &lt;abstr&gt;

nat10Real.re

module ShowNat: ShowNatGroup = {
  include Nat;
  
  let toString = n =&gt; n == zero ? &quot;IsZero&quot; : &quot;IsNotZero&quot;; 
}
// module ShowNat: ShowNatGroup;

nat11.re

ShowNat.(toString(zero)); ShowNat.(toString(succ(zero)));
// - : string = &quot;IsZero&quot;
// - : string = &quot;IsNotZero&quot;

nat12.re

module type Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let printUntil: int =&gt; unit;
};
/*
module type Nat =
  (ShowNatGroup : ShowNatGroup) =&gt; { let printUntil: int =&gt; unit; };
*/

nat13.re

module Nat: Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let rec getItem = fun
    | 0 =&gt; ShowNatGroup.zero
    | i =&gt; ShowNatGroup.succ(getItem(i - 1));
  
  let printItem = item =&gt; print_endline(ShowNatGroup.toString(item));
  
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? ShowNatGroup.toString(item) : acc ++ &quot;, &quot; ++ ShowNatGroup.toString(item);
  
  let printUntil = n =&gt; {
    let items = List.init(n, getItem);
    print_endline(List.fold_left(join, &quot;&quot;, items));
  };
};
// module Nat: Nat;

nat14.re

module NatInt = Nat({
  type t = int;
  let zero = 0;
  let succ = t =&gt; t + 1;
  let toString = string_of_int;
});
// module NatInt: { let printUntil: int =&gt; unit; };

nat15.re

module NatBool = Nat({
  type t = bool;
  let zero = false;
  let succ = _ =&gt; true;
  let toString = string_of_bool;
});
// module NatBool: { let printUntil: int =&gt; unit; };

nat16.re

module NatTern = Nat({
  type t = option(bool);
  let zero = Some(false);
  let succ = fun
    | Some(false) =&gt; None
    | _ =&gt; Some(true);
  let toString = fun
    | Some(item) =&gt; string_of_bool(item)
    | None =&gt; &quot;null&quot;;
});
// module NatTern: { let printUntil: int =&gt; unit; };

nat17.re

NatBool.printUntil(3);
// false, true, true

NatTern.printUntil(3);
// false, null, true

NatInt.printUntil(3);
// 0, 1, 2

nat18.re

module NatChurch = {
  // Here&#x27;s where we get a bit creative with how we combine our Nats.
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? item : item ++ &quot; (&quot; ++ acc ++ &quot;)&quot;;

  // Extending the Nat functor for a specialized case. This is where ReasonML&#x27;s flexibility really shines.
  include Nat({
    type t = list(string);
    let zero = [];
    let succ = t =&gt; [&quot;f&quot;, ...t];
    let toString = t =&gt; List.fold_left(join, &quot;x&quot;, t);
  });
}
/* 
module NatChurch:
  { let join: (string, string) =&gt; string; let printUntil: int =&gt; unit; };
*/

nat19.re

NatChurch.printUntil(3);
// x, f (x), f (f (x))

nat2.re

let zero: int = 0;
// let zero: int = 0;

let succ: int =&gt; int = x =&gt; x + 1;
// let succ: int =&gt; int = &lt;fun&gt;;

nat3.re

let zeroInt: natGroup(int) = zero =&gt; succ =&gt; zero;
// let zeroInt: natGroup(int) = &lt;fun&gt;;

let oneInt: natGroup(int) = zero =&gt; succ =&gt; succ (zero);
// let oneInt: natGroup(int) = &lt;fun&gt;;

let twoInt: natGroup(int) = zero =&gt; succ =&gt; succ (succ (zero));
// let twoInt: natGroup(int) = &lt;fun&gt;;

nat4.re

zeroInt(zero, succ); oneInt(zero, succ); twoInt(zero, succ);
// - : int = 0
// - : int = 1
// - : int = 2

nat5.re

module Nat = {
  type t = int;
  
  let zero: t = 0;
  let succ: t =&gt; t = x =&gt; x + 1;
}
// module Nat: { type t = int; let zero: t; let succ: t =&gt; t; };

nat6.re

Nat.(zero); Nat.(succ(zero)); Nat.(succ(succ(zero)));
// - : Nat.t = 0
// - : Nat.t = 1
// - : Nat.t = 2

nat7.re

module type NatGroup = {
  type t;
  
  let zero: t;
  let succ: t =&gt; t;
};
// module type NatGroup = { type t; let zero: t; let succ: t =&gt; t; };

nat8.re

module NatPriv: NatGroup = {
  include Nat; 
  let aPrivateMethod = () =&gt; (); // This stays within the module.
};
// module NatPriv: NatGroup;

nat9.re

module type ShowNatGroup = {
  include NatGroup;
  let toString: t =&gt; string;
}
/* 
module type ShowNatGroup =
  { type t; let zero: t; let succ: t =&gt; t; let toString: t =&gt; string; };
*/</code></pre><p>Interfaces ensure users only see what they need to, maintaining privacy.</p><pre><code>nat.re

type natGroup(&#x27;t) = &#x27;t =&gt; (&#x27;t =&gt; &#x27;t) =&gt; &#x27;t;

---

let zero: int = 0;
let succ: int =&gt; int = x =&gt; x + 1;

---

let zeroInt: natGroup(int) = zero =&gt; succ =&gt; zero;
let oneInt: natGroup(int) = zero =&gt; succ =&gt; succ (zero);
let twoInt: natGroup(int) = zero =&gt; succ =&gt; succ (succ (zero));

--- 

zeroInt(zero, succ); oneInt(zero, succ); twoInt(zero, succ);

---

module Nat = {
  type t = int;
  
  let zero: t = 0;
  let succ: t =&gt; t = x =&gt; x + 1;
}

---

Nat.(zero); Nat.(succ(zero)); Nat.(succ(succ(zero)));

---

module type NatGroup = {
  type t;
  
  let zero: t;
  let succ: t =&gt; t;
};

---

module NatPriv: NatGroup = {
  include Nat; 
  let aPrivateMethod = () =&gt; (); // This stays within the module.
};

---

module type ShowNatGroup = {
  include NatGroup;
  let toString: t =&gt; string;
}

---

module ShowNat: ShowNatGroup = {
  include Nat;
  
  let toString = n =&gt; n == zero ? &quot;IsZero&quot; : &quot;IsNotZero&quot;; 
}

---

ShowNat.(zero); ShowNat.(succ(zero)); ShowNat.(succ(succ(zero)));

---

ShowNat.(toString(zero)); ShowNat.(toString(succ(zero)));

---

module type Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let printUntil: int =&gt; unit;
};

---

module Nat: Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let rec getItem = fun
    | 0 =&gt; ShowNatGroup.zero
    | i =&gt; ShowNatGroup.succ(getItem(i - 1));
  
  let printItem = item =&gt; print_endline(ShowNatGroup.toString(item));
  
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? ShowNatGroup.toString(item) : acc ++ &quot;, &quot; ++ ShowNatGroup.toString(item);
  
  let printUntil = n =&gt; {
    let items = List.init(n, getItem);
    print_endline(List.fold_left(join, &quot;&quot;, items));
  };
};

---

module NatInt = Nat({
  type t = int;
  let zero = 0;
  let succ = t =&gt; t + 1;
  let toString = string_of_int;
});

---

module NatBool = Nat({
  type t = bool;
  let zero = false;
  let succ = _ =&gt; true;
  let toString = string_of_bool;
});

---

module NatTern = Nat({
  type t = option(bool);
  let zero = Some(false);
  let succ = fun
    | Some(false) =&gt; None
    | _ =&gt; Some(true);
  let toString = fun
    | Some(item) =&gt; string_of_bool(item)
    | None =&gt; &quot;null&quot;;
});

---

NatBool.printUntil(3);
NatTern.printUntil(3);
NatInt.printUntil(3);

---

module NatChurch = {
  // Here&#x27;s where we get a bit creative with how we combine our Nats.
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? item : item ++ &quot; (&quot; ++ acc ++ &quot;)&quot;;

  // Extending the Nat functor for a specialized case. This is where ReasonML&#x27;s flexibility really shines.
  include Nat({
    type t = list(string);
    let zero = [];
    let succ = t =&gt; [&quot;f&quot;, ...t];
    let toString = t =&gt; List.fold_left(join, &quot;x&quot;, t);
  });
}

---

NatChurch.printUntil(3); 

nat1.re

type natGroup(&#x27;t) = &#x27;t =&gt; (&#x27;t =&gt; &#x27;t) =&gt; &#x27;t;
// type natGroup(&#x27;t) = (&#x27;t, &#x27;t =&gt; &#x27;t) =&gt; &#x27;t;

nat10.re

ShowNat.(zero); ShowNat.(succ(zero)); ShowNat.(succ(succ(zero)));
// - : ShowNat.t = &lt;abstr&gt;
// - : ShowNat.t = &lt;abstr&gt;
// - : ShowNat.t = &lt;abstr&gt;

nat10Real.re

module ShowNat: ShowNatGroup = {
  include Nat;
  
  let toString = n =&gt; n == zero ? &quot;IsZero&quot; : &quot;IsNotZero&quot;; 
}
// module ShowNat: ShowNatGroup;

nat11.re

ShowNat.(toString(zero)); ShowNat.(toString(succ(zero)));
// - : string = &quot;IsZero&quot;
// - : string = &quot;IsNotZero&quot;

nat12.re

module type Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let printUntil: int =&gt; unit;
};
/*
module type Nat =
  (ShowNatGroup : ShowNatGroup) =&gt; { let printUntil: int =&gt; unit; };
*/

nat13.re

module Nat: Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let rec getItem = fun
    | 0 =&gt; ShowNatGroup.zero
    | i =&gt; ShowNatGroup.succ(getItem(i - 1));
  
  let printItem = item =&gt; print_endline(ShowNatGroup.toString(item));
  
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? ShowNatGroup.toString(item) : acc ++ &quot;, &quot; ++ ShowNatGroup.toString(item);
  
  let printUntil = n =&gt; {
    let items = List.init(n, getItem);
    print_endline(List.fold_left(join, &quot;&quot;, items));
  };
};
// module Nat: Nat;

nat14.re

module NatInt = Nat({
  type t = int;
  let zero = 0;
  let succ = t =&gt; t + 1;
  let toString = string_of_int;
});
// module NatInt: { let printUntil: int =&gt; unit; };

nat15.re

module NatBool = Nat({
  type t = bool;
  let zero = false;
  let succ = _ =&gt; true;
  let toString = string_of_bool;
});
// module NatBool: { let printUntil: int =&gt; unit; };

nat16.re

module NatTern = Nat({
  type t = option(bool);
  let zero = Some(false);
  let succ = fun
    | Some(false) =&gt; None
    | _ =&gt; Some(true);
  let toString = fun
    | Some(item) =&gt; string_of_bool(item)
    | None =&gt; &quot;null&quot;;
});
// module NatTern: { let printUntil: int =&gt; unit; };

nat17.re

NatBool.printUntil(3);
// false, true, true

NatTern.printUntil(3);
// false, null, true

NatInt.printUntil(3);
// 0, 1, 2

nat18.re

module NatChurch = {
  // Here&#x27;s where we get a bit creative with how we combine our Nats.
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? item : item ++ &quot; (&quot; ++ acc ++ &quot;)&quot;;

  // Extending the Nat functor for a specialized case. This is where ReasonML&#x27;s flexibility really shines.
  include Nat({
    type t = list(string);
    let zero = [];
    let succ = t =&gt; [&quot;f&quot;, ...t];
    let toString = t =&gt; List.fold_left(join, &quot;x&quot;, t);
  });
}
/* 
module NatChurch:
  { let join: (string, string) =&gt; string; let printUntil: int =&gt; unit; };
*/

nat19.re

NatChurch.printUntil(3);
// x, f (x), f (f (x))

nat2.re

let zero: int = 0;
// let zero: int = 0;

let succ: int =&gt; int = x =&gt; x + 1;
// let succ: int =&gt; int = &lt;fun&gt;;

nat3.re

let zeroInt: natGroup(int) = zero =&gt; succ =&gt; zero;
// let zeroInt: natGroup(int) = &lt;fun&gt;;

let oneInt: natGroup(int) = zero =&gt; succ =&gt; succ (zero);
// let oneInt: natGroup(int) = &lt;fun&gt;;

let twoInt: natGroup(int) = zero =&gt; succ =&gt; succ (succ (zero));
// let twoInt: natGroup(int) = &lt;fun&gt;;

nat4.re

zeroInt(zero, succ); oneInt(zero, succ); twoInt(zero, succ);
// - : int = 0
// - : int = 1
// - : int = 2

nat5.re

module Nat = {
  type t = int;
  
  let zero: t = 0;
  let succ: t =&gt; t = x =&gt; x + 1;
}
// module Nat: { type t = int; let zero: t; let succ: t =&gt; t; };

nat6.re

Nat.(zero); Nat.(succ(zero)); Nat.(succ(succ(zero)));
// - : Nat.t = 0
// - : Nat.t = 1
// - : Nat.t = 2

nat7.re

module type NatGroup = {
  type t;
  
  let zero: t;
  let succ: t =&gt; t;
};
// module type NatGroup = { type t; let zero: t; let succ: t =&gt; t; };

nat8.re

module NatPriv: NatGroup = {
  include Nat; 
  let aPrivateMethod = () =&gt; (); // This stays within the module.
};
// module NatPriv: NatGroup;

nat9.re

module type ShowNatGroup = {
  include NatGroup;
  let toString: t =&gt; string;
}
/* 
module type ShowNatGroup =
  { type t; let zero: t; let succ: t =&gt; t; let toString: t =&gt; string; };
*/</code></pre><p>Now, onto functors, ReasonML’s way of transforming modules. Functors take a module and return a new, tailored module. The functor interface sets the blueprint for transformation.</p><pre><code>nat.re

type natGroup(&#x27;t) = &#x27;t =&gt; (&#x27;t =&gt; &#x27;t) =&gt; &#x27;t;

---

let zero: int = 0;
let succ: int =&gt; int = x =&gt; x + 1;

---

let zeroInt: natGroup(int) = zero =&gt; succ =&gt; zero;
let oneInt: natGroup(int) = zero =&gt; succ =&gt; succ (zero);
let twoInt: natGroup(int) = zero =&gt; succ =&gt; succ (succ (zero));

--- 

zeroInt(zero, succ); oneInt(zero, succ); twoInt(zero, succ);

---

module Nat = {
  type t = int;
  
  let zero: t = 0;
  let succ: t =&gt; t = x =&gt; x + 1;
}

---

Nat.(zero); Nat.(succ(zero)); Nat.(succ(succ(zero)));

---

module type NatGroup = {
  type t;
  
  let zero: t;
  let succ: t =&gt; t;
};

---

module NatPriv: NatGroup = {
  include Nat; 
  let aPrivateMethod = () =&gt; (); // This stays within the module.
};

---

module type ShowNatGroup = {
  include NatGroup;
  let toString: t =&gt; string;
}

---

module ShowNat: ShowNatGroup = {
  include Nat;
  
  let toString = n =&gt; n == zero ? &quot;IsZero&quot; : &quot;IsNotZero&quot;; 
}

---

ShowNat.(zero); ShowNat.(succ(zero)); ShowNat.(succ(succ(zero)));

---

ShowNat.(toString(zero)); ShowNat.(toString(succ(zero)));

---

module type Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let printUntil: int =&gt; unit;
};

---

module Nat: Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let rec getItem = fun
    | 0 =&gt; ShowNatGroup.zero
    | i =&gt; ShowNatGroup.succ(getItem(i - 1));
  
  let printItem = item =&gt; print_endline(ShowNatGroup.toString(item));
  
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? ShowNatGroup.toString(item) : acc ++ &quot;, &quot; ++ ShowNatGroup.toString(item);
  
  let printUntil = n =&gt; {
    let items = List.init(n, getItem);
    print_endline(List.fold_left(join, &quot;&quot;, items));
  };
};

---

module NatInt = Nat({
  type t = int;
  let zero = 0;
  let succ = t =&gt; t + 1;
  let toString = string_of_int;
});

---

module NatBool = Nat({
  type t = bool;
  let zero = false;
  let succ = _ =&gt; true;
  let toString = string_of_bool;
});

---

module NatTern = Nat({
  type t = option(bool);
  let zero = Some(false);
  let succ = fun
    | Some(false) =&gt; None
    | _ =&gt; Some(true);
  let toString = fun
    | Some(item) =&gt; string_of_bool(item)
    | None =&gt; &quot;null&quot;;
});

---

NatBool.printUntil(3);
NatTern.printUntil(3);
NatInt.printUntil(3);

---

module NatChurch = {
  // Here&#x27;s where we get a bit creative with how we combine our Nats.
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? item : item ++ &quot; (&quot; ++ acc ++ &quot;)&quot;;

  // Extending the Nat functor for a specialized case. This is where ReasonML&#x27;s flexibility really shines.
  include Nat({
    type t = list(string);
    let zero = [];
    let succ = t =&gt; [&quot;f&quot;, ...t];
    let toString = t =&gt; List.fold_left(join, &quot;x&quot;, t);
  });
}

---

NatChurch.printUntil(3); 

nat1.re

type natGroup(&#x27;t) = &#x27;t =&gt; (&#x27;t =&gt; &#x27;t) =&gt; &#x27;t;
// type natGroup(&#x27;t) = (&#x27;t, &#x27;t =&gt; &#x27;t) =&gt; &#x27;t;

nat10.re

ShowNat.(zero); ShowNat.(succ(zero)); ShowNat.(succ(succ(zero)));
// - : ShowNat.t = &lt;abstr&gt;
// - : ShowNat.t = &lt;abstr&gt;
// - : ShowNat.t = &lt;abstr&gt;

nat10Real.re

module ShowNat: ShowNatGroup = {
  include Nat;
  
  let toString = n =&gt; n == zero ? &quot;IsZero&quot; : &quot;IsNotZero&quot;; 
}
// module ShowNat: ShowNatGroup;

nat11.re

ShowNat.(toString(zero)); ShowNat.(toString(succ(zero)));
// - : string = &quot;IsZero&quot;
// - : string = &quot;IsNotZero&quot;

nat12.re

module type Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let printUntil: int =&gt; unit;
};
/*
module type Nat =
  (ShowNatGroup : ShowNatGroup) =&gt; { let printUntil: int =&gt; unit; };
*/

nat13.re

module Nat: Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let rec getItem = fun
    | 0 =&gt; ShowNatGroup.zero
    | i =&gt; ShowNatGroup.succ(getItem(i - 1));
  
  let printItem = item =&gt; print_endline(ShowNatGroup.toString(item));
  
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? ShowNatGroup.toString(item) : acc ++ &quot;, &quot; ++ ShowNatGroup.toString(item);
  
  let printUntil = n =&gt; {
    let items = List.init(n, getItem);
    print_endline(List.fold_left(join, &quot;&quot;, items));
  };
};
// module Nat: Nat;

nat14.re

module NatInt = Nat({
  type t = int;
  let zero = 0;
  let succ = t =&gt; t + 1;
  let toString = string_of_int;
});
// module NatInt: { let printUntil: int =&gt; unit; };

nat15.re

module NatBool = Nat({
  type t = bool;
  let zero = false;
  let succ = _ =&gt; true;
  let toString = string_of_bool;
});
// module NatBool: { let printUntil: int =&gt; unit; };

nat16.re

module NatTern = Nat({
  type t = option(bool);
  let zero = Some(false);
  let succ = fun
    | Some(false) =&gt; None
    | _ =&gt; Some(true);
  let toString = fun
    | Some(item) =&gt; string_of_bool(item)
    | None =&gt; &quot;null&quot;;
});
// module NatTern: { let printUntil: int =&gt; unit; };

nat17.re

NatBool.printUntil(3);
// false, true, true

NatTern.printUntil(3);
// false, null, true

NatInt.printUntil(3);
// 0, 1, 2

nat18.re

module NatChurch = {
  // Here&#x27;s where we get a bit creative with how we combine our Nats.
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? item : item ++ &quot; (&quot; ++ acc ++ &quot;)&quot;;

  // Extending the Nat functor for a specialized case. This is where ReasonML&#x27;s flexibility really shines.
  include Nat({
    type t = list(string);
    let zero = [];
    let succ = t =&gt; [&quot;f&quot;, ...t];
    let toString = t =&gt; List.fold_left(join, &quot;x&quot;, t);
  });
}
/* 
module NatChurch:
  { let join: (string, string) =&gt; string; let printUntil: int =&gt; unit; };
*/

nat19.re

NatChurch.printUntil(3);
// x, f (x), f (f (x))

nat2.re

let zero: int = 0;
// let zero: int = 0;

let succ: int =&gt; int = x =&gt; x + 1;
// let succ: int =&gt; int = &lt;fun&gt;;

nat3.re

let zeroInt: natGroup(int) = zero =&gt; succ =&gt; zero;
// let zeroInt: natGroup(int) = &lt;fun&gt;;

let oneInt: natGroup(int) = zero =&gt; succ =&gt; succ (zero);
// let oneInt: natGroup(int) = &lt;fun&gt;;

let twoInt: natGroup(int) = zero =&gt; succ =&gt; succ (succ (zero));
// let twoInt: natGroup(int) = &lt;fun&gt;;

nat4.re

zeroInt(zero, succ); oneInt(zero, succ); twoInt(zero, succ);
// - : int = 0
// - : int = 1
// - : int = 2

nat5.re

module Nat = {
  type t = int;
  
  let zero: t = 0;
  let succ: t =&gt; t = x =&gt; x + 1;
}
// module Nat: { type t = int; let zero: t; let succ: t =&gt; t; };

nat6.re

Nat.(zero); Nat.(succ(zero)); Nat.(succ(succ(zero)));
// - : Nat.t = 0
// - : Nat.t = 1
// - : Nat.t = 2

nat7.re

module type NatGroup = {
  type t;
  
  let zero: t;
  let succ: t =&gt; t;
};
// module type NatGroup = { type t; let zero: t; let succ: t =&gt; t; };

nat8.re

module NatPriv: NatGroup = {
  include Nat; 
  let aPrivateMethod = () =&gt; (); // This stays within the module.
};
// module NatPriv: NatGroup;

nat9.re

module type ShowNatGroup = {
  include NatGroup;
  let toString: t =&gt; string;
}
/* 
module type ShowNatGroup =
  { type t; let zero: t; let succ: t =&gt; t; let toString: t =&gt; string; };
*/</code></pre><p>Implementing the functor involves crafting custom logic without using “include”.</p><pre><code>nat.re

type natGroup(&#x27;t) = &#x27;t =&gt; (&#x27;t =&gt; &#x27;t) =&gt; &#x27;t;

---

let zero: int = 0;
let succ: int =&gt; int = x =&gt; x + 1;

---

let zeroInt: natGroup(int) = zero =&gt; succ =&gt; zero;
let oneInt: natGroup(int) = zero =&gt; succ =&gt; succ (zero);
let twoInt: natGroup(int) = zero =&gt; succ =&gt; succ (succ (zero));

--- 

zeroInt(zero, succ); oneInt(zero, succ); twoInt(zero, succ);

---

module Nat = {
  type t = int;
  
  let zero: t = 0;
  let succ: t =&gt; t = x =&gt; x + 1;
}

---

Nat.(zero); Nat.(succ(zero)); Nat.(succ(succ(zero)));

---

module type NatGroup = {
  type t;
  
  let zero: t;
  let succ: t =&gt; t;
};

---

module NatPriv: NatGroup = {
  include Nat; 
  let aPrivateMethod = () =&gt; (); // This stays within the module.
};

---

module type ShowNatGroup = {
  include NatGroup;
  let toString: t =&gt; string;
}

---

module ShowNat: ShowNatGroup = {
  include Nat;
  
  let toString = n =&gt; n == zero ? &quot;IsZero&quot; : &quot;IsNotZero&quot;; 
}

---

ShowNat.(zero); ShowNat.(succ(zero)); ShowNat.(succ(succ(zero)));

---

ShowNat.(toString(zero)); ShowNat.(toString(succ(zero)));

---

module type Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let printUntil: int =&gt; unit;
};

---

module Nat: Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let rec getItem = fun
    | 0 =&gt; ShowNatGroup.zero
    | i =&gt; ShowNatGroup.succ(getItem(i - 1));
  
  let printItem = item =&gt; print_endline(ShowNatGroup.toString(item));
  
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? ShowNatGroup.toString(item) : acc ++ &quot;, &quot; ++ ShowNatGroup.toString(item);
  
  let printUntil = n =&gt; {
    let items = List.init(n, getItem);
    print_endline(List.fold_left(join, &quot;&quot;, items));
  };
};

---

module NatInt = Nat({
  type t = int;
  let zero = 0;
  let succ = t =&gt; t + 1;
  let toString = string_of_int;
});

---

module NatBool = Nat({
  type t = bool;
  let zero = false;
  let succ = _ =&gt; true;
  let toString = string_of_bool;
});

---

module NatTern = Nat({
  type t = option(bool);
  let zero = Some(false);
  let succ = fun
    | Some(false) =&gt; None
    | _ =&gt; Some(true);
  let toString = fun
    | Some(item) =&gt; string_of_bool(item)
    | None =&gt; &quot;null&quot;;
});

---

NatBool.printUntil(3);
NatTern.printUntil(3);
NatInt.printUntil(3);

---

module NatChurch = {
  // Here&#x27;s where we get a bit creative with how we combine our Nats.
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? item : item ++ &quot; (&quot; ++ acc ++ &quot;)&quot;;

  // Extending the Nat functor for a specialized case. This is where ReasonML&#x27;s flexibility really shines.
  include Nat({
    type t = list(string);
    let zero = [];
    let succ = t =&gt; [&quot;f&quot;, ...t];
    let toString = t =&gt; List.fold_left(join, &quot;x&quot;, t);
  });
}

---

NatChurch.printUntil(3); 

nat1.re

type natGroup(&#x27;t) = &#x27;t =&gt; (&#x27;t =&gt; &#x27;t) =&gt; &#x27;t;
// type natGroup(&#x27;t) = (&#x27;t, &#x27;t =&gt; &#x27;t) =&gt; &#x27;t;

nat10.re

ShowNat.(zero); ShowNat.(succ(zero)); ShowNat.(succ(succ(zero)));
// - : ShowNat.t = &lt;abstr&gt;
// - : ShowNat.t = &lt;abstr&gt;
// - : ShowNat.t = &lt;abstr&gt;

nat10Real.re

module ShowNat: ShowNatGroup = {
  include Nat;
  
  let toString = n =&gt; n == zero ? &quot;IsZero&quot; : &quot;IsNotZero&quot;; 
}
// module ShowNat: ShowNatGroup;

nat11.re

ShowNat.(toString(zero)); ShowNat.(toString(succ(zero)));
// - : string = &quot;IsZero&quot;
// - : string = &quot;IsNotZero&quot;

nat12.re

module type Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let printUntil: int =&gt; unit;
};
/*
module type Nat =
  (ShowNatGroup : ShowNatGroup) =&gt; { let printUntil: int =&gt; unit; };
*/

nat13.re

module Nat: Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let rec getItem = fun
    | 0 =&gt; ShowNatGroup.zero
    | i =&gt; ShowNatGroup.succ(getItem(i - 1));
  
  let printItem = item =&gt; print_endline(ShowNatGroup.toString(item));
  
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? ShowNatGroup.toString(item) : acc ++ &quot;, &quot; ++ ShowNatGroup.toString(item);
  
  let printUntil = n =&gt; {
    let items = List.init(n, getItem);
    print_endline(List.fold_left(join, &quot;&quot;, items));
  };
};
// module Nat: Nat;

nat14.re

module NatInt = Nat({
  type t = int;
  let zero = 0;
  let succ = t =&gt; t + 1;
  let toString = string_of_int;
});
// module NatInt: { let printUntil: int =&gt; unit; };

nat15.re

module NatBool = Nat({
  type t = bool;
  let zero = false;
  let succ = _ =&gt; true;
  let toString = string_of_bool;
});
// module NatBool: { let printUntil: int =&gt; unit; };

nat16.re

module NatTern = Nat({
  type t = option(bool);
  let zero = Some(false);
  let succ = fun
    | Some(false) =&gt; None
    | _ =&gt; Some(true);
  let toString = fun
    | Some(item) =&gt; string_of_bool(item)
    | None =&gt; &quot;null&quot;;
});
// module NatTern: { let printUntil: int =&gt; unit; };

nat17.re

NatBool.printUntil(3);
// false, true, true

NatTern.printUntil(3);
// false, null, true

NatInt.printUntil(3);
// 0, 1, 2

nat18.re

module NatChurch = {
  // Here&#x27;s where we get a bit creative with how we combine our Nats.
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? item : item ++ &quot; (&quot; ++ acc ++ &quot;)&quot;;

  // Extending the Nat functor for a specialized case. This is where ReasonML&#x27;s flexibility really shines.
  include Nat({
    type t = list(string);
    let zero = [];
    let succ = t =&gt; [&quot;f&quot;, ...t];
    let toString = t =&gt; List.fold_left(join, &quot;x&quot;, t);
  });
}
/* 
module NatChurch:
  { let join: (string, string) =&gt; string; let printUntil: int =&gt; unit; };
*/

nat19.re

NatChurch.printUntil(3);
// x, f (x), f (f (x))

nat2.re

let zero: int = 0;
// let zero: int = 0;

let succ: int =&gt; int = x =&gt; x + 1;
// let succ: int =&gt; int = &lt;fun&gt;;

nat3.re

let zeroInt: natGroup(int) = zero =&gt; succ =&gt; zero;
// let zeroInt: natGroup(int) = &lt;fun&gt;;

let oneInt: natGroup(int) = zero =&gt; succ =&gt; succ (zero);
// let oneInt: natGroup(int) = &lt;fun&gt;;

let twoInt: natGroup(int) = zero =&gt; succ =&gt; succ (succ (zero));
// let twoInt: natGroup(int) = &lt;fun&gt;;

nat4.re

zeroInt(zero, succ); oneInt(zero, succ); twoInt(zero, succ);
// - : int = 0
// - : int = 1
// - : int = 2

nat5.re

module Nat = {
  type t = int;
  
  let zero: t = 0;
  let succ: t =&gt; t = x =&gt; x + 1;
}
// module Nat: { type t = int; let zero: t; let succ: t =&gt; t; };

nat6.re

Nat.(zero); Nat.(succ(zero)); Nat.(succ(succ(zero)));
// - : Nat.t = 0
// - : Nat.t = 1
// - : Nat.t = 2

nat7.re

module type NatGroup = {
  type t;
  
  let zero: t;
  let succ: t =&gt; t;
};
// module type NatGroup = { type t; let zero: t; let succ: t =&gt; t; };

nat8.re

module NatPriv: NatGroup = {
  include Nat; 
  let aPrivateMethod = () =&gt; (); // This stays within the module.
};
// module NatPriv: NatGroup;

nat9.re

module type ShowNatGroup = {
  include NatGroup;
  let toString: t =&gt; string;
}
/* 
module type ShowNatGroup =
  { type t; let zero: t; let succ: t =&gt; t; let toString: t =&gt; string; };
*/</code></pre><p>With NatInt, you’re applying the functor to integer types for a sleek implementation.</p><pre><code>nat.re

type natGroup(&#x27;t) = &#x27;t =&gt; (&#x27;t =&gt; &#x27;t) =&gt; &#x27;t;

---

let zero: int = 0;
let succ: int =&gt; int = x =&gt; x + 1;

---

let zeroInt: natGroup(int) = zero =&gt; succ =&gt; zero;
let oneInt: natGroup(int) = zero =&gt; succ =&gt; succ (zero);
let twoInt: natGroup(int) = zero =&gt; succ =&gt; succ (succ (zero));

--- 

zeroInt(zero, succ); oneInt(zero, succ); twoInt(zero, succ);

---

module Nat = {
  type t = int;
  
  let zero: t = 0;
  let succ: t =&gt; t = x =&gt; x + 1;
}

---

Nat.(zero); Nat.(succ(zero)); Nat.(succ(succ(zero)));

---

module type NatGroup = {
  type t;
  
  let zero: t;
  let succ: t =&gt; t;
};

---

module NatPriv: NatGroup = {
  include Nat; 
  let aPrivateMethod = () =&gt; (); // This stays within the module.
};

---

module type ShowNatGroup = {
  include NatGroup;
  let toString: t =&gt; string;
}

---

module ShowNat: ShowNatGroup = {
  include Nat;
  
  let toString = n =&gt; n == zero ? &quot;IsZero&quot; : &quot;IsNotZero&quot;; 
}

---

ShowNat.(zero); ShowNat.(succ(zero)); ShowNat.(succ(succ(zero)));

---

ShowNat.(toString(zero)); ShowNat.(toString(succ(zero)));

---

module type Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let printUntil: int =&gt; unit;
};

---

module Nat: Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let rec getItem = fun
    | 0 =&gt; ShowNatGroup.zero
    | i =&gt; ShowNatGroup.succ(getItem(i - 1));
  
  let printItem = item =&gt; print_endline(ShowNatGroup.toString(item));
  
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? ShowNatGroup.toString(item) : acc ++ &quot;, &quot; ++ ShowNatGroup.toString(item);
  
  let printUntil = n =&gt; {
    let items = List.init(n, getItem);
    print_endline(List.fold_left(join, &quot;&quot;, items));
  };
};

---

module NatInt = Nat({
  type t = int;
  let zero = 0;
  let succ = t =&gt; t + 1;
  let toString = string_of_int;
});

---

module NatBool = Nat({
  type t = bool;
  let zero = false;
  let succ = _ =&gt; true;
  let toString = string_of_bool;
});

---

module NatTern = Nat({
  type t = option(bool);
  let zero = Some(false);
  let succ = fun
    | Some(false) =&gt; None
    | _ =&gt; Some(true);
  let toString = fun
    | Some(item) =&gt; string_of_bool(item)
    | None =&gt; &quot;null&quot;;
});

---

NatBool.printUntil(3);
NatTern.printUntil(3);
NatInt.printUntil(3);

---

module NatChurch = {
  // Here&#x27;s where we get a bit creative with how we combine our Nats.
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? item : item ++ &quot; (&quot; ++ acc ++ &quot;)&quot;;

  // Extending the Nat functor for a specialized case. This is where ReasonML&#x27;s flexibility really shines.
  include Nat({
    type t = list(string);
    let zero = [];
    let succ = t =&gt; [&quot;f&quot;, ...t];
    let toString = t =&gt; List.fold_left(join, &quot;x&quot;, t);
  });
}

---

NatChurch.printUntil(3); 

nat1.re

type natGroup(&#x27;t) = &#x27;t =&gt; (&#x27;t =&gt; &#x27;t) =&gt; &#x27;t;
// type natGroup(&#x27;t) = (&#x27;t, &#x27;t =&gt; &#x27;t) =&gt; &#x27;t;

nat10.re

ShowNat.(zero); ShowNat.(succ(zero)); ShowNat.(succ(succ(zero)));
// - : ShowNat.t = &lt;abstr&gt;
// - : ShowNat.t = &lt;abstr&gt;
// - : ShowNat.t = &lt;abstr&gt;

nat10Real.re

module ShowNat: ShowNatGroup = {
  include Nat;
  
  let toString = n =&gt; n == zero ? &quot;IsZero&quot; : &quot;IsNotZero&quot;; 
}
// module ShowNat: ShowNatGroup;

nat11.re

ShowNat.(toString(zero)); ShowNat.(toString(succ(zero)));
// - : string = &quot;IsZero&quot;
// - : string = &quot;IsNotZero&quot;

nat12.re

module type Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let printUntil: int =&gt; unit;
};
/*
module type Nat =
  (ShowNatGroup : ShowNatGroup) =&gt; { let printUntil: int =&gt; unit; };
*/

nat13.re

module Nat: Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let rec getItem = fun
    | 0 =&gt; ShowNatGroup.zero
    | i =&gt; ShowNatGroup.succ(getItem(i - 1));
  
  let printItem = item =&gt; print_endline(ShowNatGroup.toString(item));
  
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? ShowNatGroup.toString(item) : acc ++ &quot;, &quot; ++ ShowNatGroup.toString(item);
  
  let printUntil = n =&gt; {
    let items = List.init(n, getItem);
    print_endline(List.fold_left(join, &quot;&quot;, items));
  };
};
// module Nat: Nat;

nat14.re

module NatInt = Nat({
  type t = int;
  let zero = 0;
  let succ = t =&gt; t + 1;
  let toString = string_of_int;
});
// module NatInt: { let printUntil: int =&gt; unit; };

nat15.re

module NatBool = Nat({
  type t = bool;
  let zero = false;
  let succ = _ =&gt; true;
  let toString = string_of_bool;
});
// module NatBool: { let printUntil: int =&gt; unit; };

nat16.re

module NatTern = Nat({
  type t = option(bool);
  let zero = Some(false);
  let succ = fun
    | Some(false) =&gt; None
    | _ =&gt; Some(true);
  let toString = fun
    | Some(item) =&gt; string_of_bool(item)
    | None =&gt; &quot;null&quot;;
});
// module NatTern: { let printUntil: int =&gt; unit; };

nat17.re

NatBool.printUntil(3);
// false, true, true

NatTern.printUntil(3);
// false, null, true

NatInt.printUntil(3);
// 0, 1, 2

nat18.re

module NatChurch = {
  // Here&#x27;s where we get a bit creative with how we combine our Nats.
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? item : item ++ &quot; (&quot; ++ acc ++ &quot;)&quot;;

  // Extending the Nat functor for a specialized case. This is where ReasonML&#x27;s flexibility really shines.
  include Nat({
    type t = list(string);
    let zero = [];
    let succ = t =&gt; [&quot;f&quot;, ...t];
    let toString = t =&gt; List.fold_left(join, &quot;x&quot;, t);
  });
}
/* 
module NatChurch:
  { let join: (string, string) =&gt; string; let printUntil: int =&gt; unit; };
*/

nat19.re

NatChurch.printUntil(3);
// x, f (x), f (f (x))

nat2.re

let zero: int = 0;
// let zero: int = 0;

let succ: int =&gt; int = x =&gt; x + 1;
// let succ: int =&gt; int = &lt;fun&gt;;

nat3.re

let zeroInt: natGroup(int) = zero =&gt; succ =&gt; zero;
// let zeroInt: natGroup(int) = &lt;fun&gt;;

let oneInt: natGroup(int) = zero =&gt; succ =&gt; succ (zero);
// let oneInt: natGroup(int) = &lt;fun&gt;;

let twoInt: natGroup(int) = zero =&gt; succ =&gt; succ (succ (zero));
// let twoInt: natGroup(int) = &lt;fun&gt;;

nat4.re

zeroInt(zero, succ); oneInt(zero, succ); twoInt(zero, succ);
// - : int = 0
// - : int = 1
// - : int = 2

nat5.re

module Nat = {
  type t = int;
  
  let zero: t = 0;
  let succ: t =&gt; t = x =&gt; x + 1;
}
// module Nat: { type t = int; let zero: t; let succ: t =&gt; t; };

nat6.re

Nat.(zero); Nat.(succ(zero)); Nat.(succ(succ(zero)));
// - : Nat.t = 0
// - : Nat.t = 1
// - : Nat.t = 2

nat7.re

module type NatGroup = {
  type t;
  
  let zero: t;
  let succ: t =&gt; t;
};
// module type NatGroup = { type t; let zero: t; let succ: t =&gt; t; };

nat8.re

module NatPriv: NatGroup = {
  include Nat; 
  let aPrivateMethod = () =&gt; (); // This stays within the module.
};
// module NatPriv: NatGroup;

nat9.re

module type ShowNatGroup = {
  include NatGroup;
  let toString: t =&gt; string;
}
/* 
module type ShowNatGroup =
  { type t; let zero: t; let succ: t =&gt; t; let toString: t =&gt; string; };
*/</code></pre><p>NatBool applies the same logic to booleans, showing off the functor’s versatility.</p><pre><code>nat.re

type natGroup(&#x27;t) = &#x27;t =&gt; (&#x27;t =&gt; &#x27;t) =&gt; &#x27;t;

---

let zero: int = 0;
let succ: int =&gt; int = x =&gt; x + 1;

---

let zeroInt: natGroup(int) = zero =&gt; succ =&gt; zero;
let oneInt: natGroup(int) = zero =&gt; succ =&gt; succ (zero);
let twoInt: natGroup(int) = zero =&gt; succ =&gt; succ (succ (zero));

--- 

zeroInt(zero, succ); oneInt(zero, succ); twoInt(zero, succ);

---

module Nat = {
  type t = int;
  
  let zero: t = 0;
  let succ: t =&gt; t = x =&gt; x + 1;
}

---

Nat.(zero); Nat.(succ(zero)); Nat.(succ(succ(zero)));

---

module type NatGroup = {
  type t;
  
  let zero: t;
  let succ: t =&gt; t;
};

---

module NatPriv: NatGroup = {
  include Nat; 
  let aPrivateMethod = () =&gt; (); // This stays within the module.
};

---

module type ShowNatGroup = {
  include NatGroup;
  let toString: t =&gt; string;
}

---

module ShowNat: ShowNatGroup = {
  include Nat;
  
  let toString = n =&gt; n == zero ? &quot;IsZero&quot; : &quot;IsNotZero&quot;; 
}

---

ShowNat.(zero); ShowNat.(succ(zero)); ShowNat.(succ(succ(zero)));

---

ShowNat.(toString(zero)); ShowNat.(toString(succ(zero)));

---

module type Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let printUntil: int =&gt; unit;
};

---

module Nat: Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let rec getItem = fun
    | 0 =&gt; ShowNatGroup.zero
    | i =&gt; ShowNatGroup.succ(getItem(i - 1));
  
  let printItem = item =&gt; print_endline(ShowNatGroup.toString(item));
  
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? ShowNatGroup.toString(item) : acc ++ &quot;, &quot; ++ ShowNatGroup.toString(item);
  
  let printUntil = n =&gt; {
    let items = List.init(n, getItem);
    print_endline(List.fold_left(join, &quot;&quot;, items));
  };
};

---

module NatInt = Nat({
  type t = int;
  let zero = 0;
  let succ = t =&gt; t + 1;
  let toString = string_of_int;
});

---

module NatBool = Nat({
  type t = bool;
  let zero = false;
  let succ = _ =&gt; true;
  let toString = string_of_bool;
});

---

module NatTern = Nat({
  type t = option(bool);
  let zero = Some(false);
  let succ = fun
    | Some(false) =&gt; None
    | _ =&gt; Some(true);
  let toString = fun
    | Some(item) =&gt; string_of_bool(item)
    | None =&gt; &quot;null&quot;;
});

---

NatBool.printUntil(3);
NatTern.printUntil(3);
NatInt.printUntil(3);

---

module NatChurch = {
  // Here&#x27;s where we get a bit creative with how we combine our Nats.
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? item : item ++ &quot; (&quot; ++ acc ++ &quot;)&quot;;

  // Extending the Nat functor for a specialized case. This is where ReasonML&#x27;s flexibility really shines.
  include Nat({
    type t = list(string);
    let zero = [];
    let succ = t =&gt; [&quot;f&quot;, ...t];
    let toString = t =&gt; List.fold_left(join, &quot;x&quot;, t);
  });
}

---

NatChurch.printUntil(3); 

nat1.re

type natGroup(&#x27;t) = &#x27;t =&gt; (&#x27;t =&gt; &#x27;t) =&gt; &#x27;t;
// type natGroup(&#x27;t) = (&#x27;t, &#x27;t =&gt; &#x27;t) =&gt; &#x27;t;

nat10.re

ShowNat.(zero); ShowNat.(succ(zero)); ShowNat.(succ(succ(zero)));
// - : ShowNat.t = &lt;abstr&gt;
// - : ShowNat.t = &lt;abstr&gt;
// - : ShowNat.t = &lt;abstr&gt;

nat10Real.re

module ShowNat: ShowNatGroup = {
  include Nat;
  
  let toString = n =&gt; n == zero ? &quot;IsZero&quot; : &quot;IsNotZero&quot;; 
}
// module ShowNat: ShowNatGroup;

nat11.re

ShowNat.(toString(zero)); ShowNat.(toString(succ(zero)));
// - : string = &quot;IsZero&quot;
// - : string = &quot;IsNotZero&quot;

nat12.re

module type Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let printUntil: int =&gt; unit;
};
/*
module type Nat =
  (ShowNatGroup : ShowNatGroup) =&gt; { let printUntil: int =&gt; unit; };
*/

nat13.re

module Nat: Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let rec getItem = fun
    | 0 =&gt; ShowNatGroup.zero
    | i =&gt; ShowNatGroup.succ(getItem(i - 1));
  
  let printItem = item =&gt; print_endline(ShowNatGroup.toString(item));
  
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? ShowNatGroup.toString(item) : acc ++ &quot;, &quot; ++ ShowNatGroup.toString(item);
  
  let printUntil = n =&gt; {
    let items = List.init(n, getItem);
    print_endline(List.fold_left(join, &quot;&quot;, items));
  };
};
// module Nat: Nat;

nat14.re

module NatInt = Nat({
  type t = int;
  let zero = 0;
  let succ = t =&gt; t + 1;
  let toString = string_of_int;
});
// module NatInt: { let printUntil: int =&gt; unit; };

nat15.re

module NatBool = Nat({
  type t = bool;
  let zero = false;
  let succ = _ =&gt; true;
  let toString = string_of_bool;
});
// module NatBool: { let printUntil: int =&gt; unit; };

nat16.re

module NatTern = Nat({
  type t = option(bool);
  let zero = Some(false);
  let succ = fun
    | Some(false) =&gt; None
    | _ =&gt; Some(true);
  let toString = fun
    | Some(item) =&gt; string_of_bool(item)
    | None =&gt; &quot;null&quot;;
});
// module NatTern: { let printUntil: int =&gt; unit; };

nat17.re

NatBool.printUntil(3);
// false, true, true

NatTern.printUntil(3);
// false, null, true

NatInt.printUntil(3);
// 0, 1, 2

nat18.re

module NatChurch = {
  // Here&#x27;s where we get a bit creative with how we combine our Nats.
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? item : item ++ &quot; (&quot; ++ acc ++ &quot;)&quot;;

  // Extending the Nat functor for a specialized case. This is where ReasonML&#x27;s flexibility really shines.
  include Nat({
    type t = list(string);
    let zero = [];
    let succ = t =&gt; [&quot;f&quot;, ...t];
    let toString = t =&gt; List.fold_left(join, &quot;x&quot;, t);
  });
}
/* 
module NatChurch:
  { let join: (string, string) =&gt; string; let printUntil: int =&gt; unit; };
*/

nat19.re

NatChurch.printUntil(3);
// x, f (x), f (f (x))

nat2.re

let zero: int = 0;
// let zero: int = 0;

let succ: int =&gt; int = x =&gt; x + 1;
// let succ: int =&gt; int = &lt;fun&gt;;

nat3.re

let zeroInt: natGroup(int) = zero =&gt; succ =&gt; zero;
// let zeroInt: natGroup(int) = &lt;fun&gt;;

let oneInt: natGroup(int) = zero =&gt; succ =&gt; succ (zero);
// let oneInt: natGroup(int) = &lt;fun&gt;;

let twoInt: natGroup(int) = zero =&gt; succ =&gt; succ (succ (zero));
// let twoInt: natGroup(int) = &lt;fun&gt;;

nat4.re

zeroInt(zero, succ); oneInt(zero, succ); twoInt(zero, succ);
// - : int = 0
// - : int = 1
// - : int = 2

nat5.re

module Nat = {
  type t = int;
  
  let zero: t = 0;
  let succ: t =&gt; t = x =&gt; x + 1;
}
// module Nat: { type t = int; let zero: t; let succ: t =&gt; t; };

nat6.re

Nat.(zero); Nat.(succ(zero)); Nat.(succ(succ(zero)));
// - : Nat.t = 0
// - : Nat.t = 1
// - : Nat.t = 2

nat7.re

module type NatGroup = {
  type t;
  
  let zero: t;
  let succ: t =&gt; t;
};
// module type NatGroup = { type t; let zero: t; let succ: t =&gt; t; };

nat8.re

module NatPriv: NatGroup = {
  include Nat; 
  let aPrivateMethod = () =&gt; (); // This stays within the module.
};
// module NatPriv: NatGroup;

nat9.re

module type ShowNatGroup = {
  include NatGroup;
  let toString: t =&gt; string;
}
/* 
module type ShowNatGroup =
  { type t; let zero: t; let succ: t =&gt; t; let toString: t =&gt; string; };
*/</code></pre><p>And for a bit of a twist, NatTern demonstrates how you can handle ternary logic, introducing a nuanced state with “null”.</p><pre><code>nat.re

type natGroup(&#x27;t) = &#x27;t =&gt; (&#x27;t =&gt; &#x27;t) =&gt; &#x27;t;

---

let zero: int = 0;
let succ: int =&gt; int = x =&gt; x + 1;

---

let zeroInt: natGroup(int) = zero =&gt; succ =&gt; zero;
let oneInt: natGroup(int) = zero =&gt; succ =&gt; succ (zero);
let twoInt: natGroup(int) = zero =&gt; succ =&gt; succ (succ (zero));

--- 

zeroInt(zero, succ); oneInt(zero, succ); twoInt(zero, succ);

---

module Nat = {
  type t = int;
  
  let zero: t = 0;
  let succ: t =&gt; t = x =&gt; x + 1;
}

---

Nat.(zero); Nat.(succ(zero)); Nat.(succ(succ(zero)));

---

module type NatGroup = {
  type t;
  
  let zero: t;
  let succ: t =&gt; t;
};

---

module NatPriv: NatGroup = {
  include Nat; 
  let aPrivateMethod = () =&gt; (); // This stays within the module.
};

---

module type ShowNatGroup = {
  include NatGroup;
  let toString: t =&gt; string;
}

---

module ShowNat: ShowNatGroup = {
  include Nat;
  
  let toString = n =&gt; n == zero ? &quot;IsZero&quot; : &quot;IsNotZero&quot;; 
}

---

ShowNat.(zero); ShowNat.(succ(zero)); ShowNat.(succ(succ(zero)));

---

ShowNat.(toString(zero)); ShowNat.(toString(succ(zero)));

---

module type Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let printUntil: int =&gt; unit;
};

---

module Nat: Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let rec getItem = fun
    | 0 =&gt; ShowNatGroup.zero
    | i =&gt; ShowNatGroup.succ(getItem(i - 1));
  
  let printItem = item =&gt; print_endline(ShowNatGroup.toString(item));
  
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? ShowNatGroup.toString(item) : acc ++ &quot;, &quot; ++ ShowNatGroup.toString(item);
  
  let printUntil = n =&gt; {
    let items = List.init(n, getItem);
    print_endline(List.fold_left(join, &quot;&quot;, items));
  };
};

---

module NatInt = Nat({
  type t = int;
  let zero = 0;
  let succ = t =&gt; t + 1;
  let toString = string_of_int;
});

---

module NatBool = Nat({
  type t = bool;
  let zero = false;
  let succ = _ =&gt; true;
  let toString = string_of_bool;
});

---

module NatTern = Nat({
  type t = option(bool);
  let zero = Some(false);
  let succ = fun
    | Some(false) =&gt; None
    | _ =&gt; Some(true);
  let toString = fun
    | Some(item) =&gt; string_of_bool(item)
    | None =&gt; &quot;null&quot;;
});

---

NatBool.printUntil(3);
NatTern.printUntil(3);
NatInt.printUntil(3);

---

module NatChurch = {
  // Here&#x27;s where we get a bit creative with how we combine our Nats.
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? item : item ++ &quot; (&quot; ++ acc ++ &quot;)&quot;;

  // Extending the Nat functor for a specialized case. This is where ReasonML&#x27;s flexibility really shines.
  include Nat({
    type t = list(string);
    let zero = [];
    let succ = t =&gt; [&quot;f&quot;, ...t];
    let toString = t =&gt; List.fold_left(join, &quot;x&quot;, t);
  });
}

---

NatChurch.printUntil(3); 

nat1.re

type natGroup(&#x27;t) = &#x27;t =&gt; (&#x27;t =&gt; &#x27;t) =&gt; &#x27;t;
// type natGroup(&#x27;t) = (&#x27;t, &#x27;t =&gt; &#x27;t) =&gt; &#x27;t;

nat10.re

ShowNat.(zero); ShowNat.(succ(zero)); ShowNat.(succ(succ(zero)));
// - : ShowNat.t = &lt;abstr&gt;
// - : ShowNat.t = &lt;abstr&gt;
// - : ShowNat.t = &lt;abstr&gt;

nat10Real.re

module ShowNat: ShowNatGroup = {
  include Nat;
  
  let toString = n =&gt; n == zero ? &quot;IsZero&quot; : &quot;IsNotZero&quot;; 
}
// module ShowNat: ShowNatGroup;

nat11.re

ShowNat.(toString(zero)); ShowNat.(toString(succ(zero)));
// - : string = &quot;IsZero&quot;
// - : string = &quot;IsNotZero&quot;

nat12.re

module type Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let printUntil: int =&gt; unit;
};
/*
module type Nat =
  (ShowNatGroup : ShowNatGroup) =&gt; { let printUntil: int =&gt; unit; };
*/

nat13.re

module Nat: Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let rec getItem = fun
    | 0 =&gt; ShowNatGroup.zero
    | i =&gt; ShowNatGroup.succ(getItem(i - 1));
  
  let printItem = item =&gt; print_endline(ShowNatGroup.toString(item));
  
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? ShowNatGroup.toString(item) : acc ++ &quot;, &quot; ++ ShowNatGroup.toString(item);
  
  let printUntil = n =&gt; {
    let items = List.init(n, getItem);
    print_endline(List.fold_left(join, &quot;&quot;, items));
  };
};
// module Nat: Nat;

nat14.re

module NatInt = Nat({
  type t = int;
  let zero = 0;
  let succ = t =&gt; t + 1;
  let toString = string_of_int;
});
// module NatInt: { let printUntil: int =&gt; unit; };

nat15.re

module NatBool = Nat({
  type t = bool;
  let zero = false;
  let succ = _ =&gt; true;
  let toString = string_of_bool;
});
// module NatBool: { let printUntil: int =&gt; unit; };

nat16.re

module NatTern = Nat({
  type t = option(bool);
  let zero = Some(false);
  let succ = fun
    | Some(false) =&gt; None
    | _ =&gt; Some(true);
  let toString = fun
    | Some(item) =&gt; string_of_bool(item)
    | None =&gt; &quot;null&quot;;
});
// module NatTern: { let printUntil: int =&gt; unit; };

nat17.re

NatBool.printUntil(3);
// false, true, true

NatTern.printUntil(3);
// false, null, true

NatInt.printUntil(3);
// 0, 1, 2

nat18.re

module NatChurch = {
  // Here&#x27;s where we get a bit creative with how we combine our Nats.
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? item : item ++ &quot; (&quot; ++ acc ++ &quot;)&quot;;

  // Extending the Nat functor for a specialized case. This is where ReasonML&#x27;s flexibility really shines.
  include Nat({
    type t = list(string);
    let zero = [];
    let succ = t =&gt; [&quot;f&quot;, ...t];
    let toString = t =&gt; List.fold_left(join, &quot;x&quot;, t);
  });
}
/* 
module NatChurch:
  { let join: (string, string) =&gt; string; let printUntil: int =&gt; unit; };
*/

nat19.re

NatChurch.printUntil(3);
// x, f (x), f (f (x))

nat2.re

let zero: int = 0;
// let zero: int = 0;

let succ: int =&gt; int = x =&gt; x + 1;
// let succ: int =&gt; int = &lt;fun&gt;;

nat3.re

let zeroInt: natGroup(int) = zero =&gt; succ =&gt; zero;
// let zeroInt: natGroup(int) = &lt;fun&gt;;

let oneInt: natGroup(int) = zero =&gt; succ =&gt; succ (zero);
// let oneInt: natGroup(int) = &lt;fun&gt;;

let twoInt: natGroup(int) = zero =&gt; succ =&gt; succ (succ (zero));
// let twoInt: natGroup(int) = &lt;fun&gt;;

nat4.re

zeroInt(zero, succ); oneInt(zero, succ); twoInt(zero, succ);
// - : int = 0
// - : int = 1
// - : int = 2

nat5.re

module Nat = {
  type t = int;
  
  let zero: t = 0;
  let succ: t =&gt; t = x =&gt; x + 1;
}
// module Nat: { type t = int; let zero: t; let succ: t =&gt; t; };

nat6.re

Nat.(zero); Nat.(succ(zero)); Nat.(succ(succ(zero)));
// - : Nat.t = 0
// - : Nat.t = 1
// - : Nat.t = 2

nat7.re

module type NatGroup = {
  type t;
  
  let zero: t;
  let succ: t =&gt; t;
};
// module type NatGroup = { type t; let zero: t; let succ: t =&gt; t; };

nat8.re

module NatPriv: NatGroup = {
  include Nat; 
  let aPrivateMethod = () =&gt; (); // This stays within the module.
};
// module NatPriv: NatGroup;

nat9.re

module type ShowNatGroup = {
  include NatGroup;
  let toString: t =&gt; string;
}
/* 
module type ShowNatGroup =
  { type t; let zero: t; let succ: t =&gt; t; let toString: t =&gt; string; };
*/</code></pre><p>Checking out the implementation in action with NatBool and NatTern, it’s clear how functors bring a level of dynamism and reusability to the table.</p><pre><code>nat.re

type natGroup(&#x27;t) = &#x27;t =&gt; (&#x27;t =&gt; &#x27;t) =&gt; &#x27;t;

---

let zero: int = 0;
let succ: int =&gt; int = x =&gt; x + 1;

---

let zeroInt: natGroup(int) = zero =&gt; succ =&gt; zero;
let oneInt: natGroup(int) = zero =&gt; succ =&gt; succ (zero);
let twoInt: natGroup(int) = zero =&gt; succ =&gt; succ (succ (zero));

--- 

zeroInt(zero, succ); oneInt(zero, succ); twoInt(zero, succ);

---

module Nat = {
  type t = int;
  
  let zero: t = 0;
  let succ: t =&gt; t = x =&gt; x + 1;
}

---

Nat.(zero); Nat.(succ(zero)); Nat.(succ(succ(zero)));

---

module type NatGroup = {
  type t;
  
  let zero: t;
  let succ: t =&gt; t;
};

---

module NatPriv: NatGroup = {
  include Nat; 
  let aPrivateMethod = () =&gt; (); // This stays within the module.
};

---

module type ShowNatGroup = {
  include NatGroup;
  let toString: t =&gt; string;
}

---

module ShowNat: ShowNatGroup = {
  include Nat;
  
  let toString = n =&gt; n == zero ? &quot;IsZero&quot; : &quot;IsNotZero&quot;; 
}

---

ShowNat.(zero); ShowNat.(succ(zero)); ShowNat.(succ(succ(zero)));

---

ShowNat.(toString(zero)); ShowNat.(toString(succ(zero)));

---

module type Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let printUntil: int =&gt; unit;
};

---

module Nat: Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let rec getItem = fun
    | 0 =&gt; ShowNatGroup.zero
    | i =&gt; ShowNatGroup.succ(getItem(i - 1));
  
  let printItem = item =&gt; print_endline(ShowNatGroup.toString(item));
  
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? ShowNatGroup.toString(item) : acc ++ &quot;, &quot; ++ ShowNatGroup.toString(item);
  
  let printUntil = n =&gt; {
    let items = List.init(n, getItem);
    print_endline(List.fold_left(join, &quot;&quot;, items));
  };
};

---

module NatInt = Nat({
  type t = int;
  let zero = 0;
  let succ = t =&gt; t + 1;
  let toString = string_of_int;
});

---

module NatBool = Nat({
  type t = bool;
  let zero = false;
  let succ = _ =&gt; true;
  let toString = string_of_bool;
});

---

module NatTern = Nat({
  type t = option(bool);
  let zero = Some(false);
  let succ = fun
    | Some(false) =&gt; None
    | _ =&gt; Some(true);
  let toString = fun
    | Some(item) =&gt; string_of_bool(item)
    | None =&gt; &quot;null&quot;;
});

---

NatBool.printUntil(3);
NatTern.printUntil(3);
NatInt.printUntil(3);

---

module NatChurch = {
  // Here&#x27;s where we get a bit creative with how we combine our Nats.
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? item : item ++ &quot; (&quot; ++ acc ++ &quot;)&quot;;

  // Extending the Nat functor for a specialized case. This is where ReasonML&#x27;s flexibility really shines.
  include Nat({
    type t = list(string);
    let zero = [];
    let succ = t =&gt; [&quot;f&quot;, ...t];
    let toString = t =&gt; List.fold_left(join, &quot;x&quot;, t);
  });
}

---

NatChurch.printUntil(3); 

nat1.re

type natGroup(&#x27;t) = &#x27;t =&gt; (&#x27;t =&gt; &#x27;t) =&gt; &#x27;t;
// type natGroup(&#x27;t) = (&#x27;t, &#x27;t =&gt; &#x27;t) =&gt; &#x27;t;

nat10.re

ShowNat.(zero); ShowNat.(succ(zero)); ShowNat.(succ(succ(zero)));
// - : ShowNat.t = &lt;abstr&gt;
// - : ShowNat.t = &lt;abstr&gt;
// - : ShowNat.t = &lt;abstr&gt;

nat10Real.re

module ShowNat: ShowNatGroup = {
  include Nat;
  
  let toString = n =&gt; n == zero ? &quot;IsZero&quot; : &quot;IsNotZero&quot;; 
}
// module ShowNat: ShowNatGroup;

nat11.re

ShowNat.(toString(zero)); ShowNat.(toString(succ(zero)));
// - : string = &quot;IsZero&quot;
// - : string = &quot;IsNotZero&quot;

nat12.re

module type Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let printUntil: int =&gt; unit;
};
/*
module type Nat =
  (ShowNatGroup : ShowNatGroup) =&gt; { let printUntil: int =&gt; unit; };
*/

nat13.re

module Nat: Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let rec getItem = fun
    | 0 =&gt; ShowNatGroup.zero
    | i =&gt; ShowNatGroup.succ(getItem(i - 1));
  
  let printItem = item =&gt; print_endline(ShowNatGroup.toString(item));
  
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? ShowNatGroup.toString(item) : acc ++ &quot;, &quot; ++ ShowNatGroup.toString(item);
  
  let printUntil = n =&gt; {
    let items = List.init(n, getItem);
    print_endline(List.fold_left(join, &quot;&quot;, items));
  };
};
// module Nat: Nat;

nat14.re

module NatInt = Nat({
  type t = int;
  let zero = 0;
  let succ = t =&gt; t + 1;
  let toString = string_of_int;
});
// module NatInt: { let printUntil: int =&gt; unit; };

nat15.re

module NatBool = Nat({
  type t = bool;
  let zero = false;
  let succ = _ =&gt; true;
  let toString = string_of_bool;
});
// module NatBool: { let printUntil: int =&gt; unit; };

nat16.re

module NatTern = Nat({
  type t = option(bool);
  let zero = Some(false);
  let succ = fun
    | Some(false) =&gt; None
    | _ =&gt; Some(true);
  let toString = fun
    | Some(item) =&gt; string_of_bool(item)
    | None =&gt; &quot;null&quot;;
});
// module NatTern: { let printUntil: int =&gt; unit; };

nat17.re

NatBool.printUntil(3);
// false, true, true

NatTern.printUntil(3);
// false, null, true

NatInt.printUntil(3);
// 0, 1, 2

nat18.re

module NatChurch = {
  // Here&#x27;s where we get a bit creative with how we combine our Nats.
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? item : item ++ &quot; (&quot; ++ acc ++ &quot;)&quot;;

  // Extending the Nat functor for a specialized case. This is where ReasonML&#x27;s flexibility really shines.
  include Nat({
    type t = list(string);
    let zero = [];
    let succ = t =&gt; [&quot;f&quot;, ...t];
    let toString = t =&gt; List.fold_left(join, &quot;x&quot;, t);
  });
}
/* 
module NatChurch:
  { let join: (string, string) =&gt; string; let printUntil: int =&gt; unit; };
*/

nat19.re

NatChurch.printUntil(3);
// x, f (x), f (f (x))

nat2.re

let zero: int = 0;
// let zero: int = 0;

let succ: int =&gt; int = x =&gt; x + 1;
// let succ: int =&gt; int = &lt;fun&gt;;

nat3.re

let zeroInt: natGroup(int) = zero =&gt; succ =&gt; zero;
// let zeroInt: natGroup(int) = &lt;fun&gt;;

let oneInt: natGroup(int) = zero =&gt; succ =&gt; succ (zero);
// let oneInt: natGroup(int) = &lt;fun&gt;;

let twoInt: natGroup(int) = zero =&gt; succ =&gt; succ (succ (zero));
// let twoInt: natGroup(int) = &lt;fun&gt;;

nat4.re

zeroInt(zero, succ); oneInt(zero, succ); twoInt(zero, succ);
// - : int = 0
// - : int = 1
// - : int = 2

nat5.re

module Nat = {
  type t = int;
  
  let zero: t = 0;
  let succ: t =&gt; t = x =&gt; x + 1;
}
// module Nat: { type t = int; let zero: t; let succ: t =&gt; t; };

nat6.re

Nat.(zero); Nat.(succ(zero)); Nat.(succ(succ(zero)));
// - : Nat.t = 0
// - : Nat.t = 1
// - : Nat.t = 2

nat7.re

module type NatGroup = {
  type t;
  
  let zero: t;
  let succ: t =&gt; t;
};
// module type NatGroup = { type t; let zero: t; let succ: t =&gt; t; };

nat8.re

module NatPriv: NatGroup = {
  include Nat; 
  let aPrivateMethod = () =&gt; (); // This stays within the module.
};
// module NatPriv: NatGroup;

nat9.re

module type ShowNatGroup = {
  include NatGroup;
  let toString: t =&gt; string;
}
/* 
module type ShowNatGroup =
  { type t; let zero: t; let succ: t =&gt; t; let toString: t =&gt; string; };
*/</code></pre><p>Suppose there’s a special case for NatChurch that needs a unique method for creating Nats, illustrating the power of extending modules.</p><pre><code>nat.re

type natGroup(&#x27;t) = &#x27;t =&gt; (&#x27;t =&gt; &#x27;t) =&gt; &#x27;t;

---

let zero: int = 0;
let succ: int =&gt; int = x =&gt; x + 1;

---

let zeroInt: natGroup(int) = zero =&gt; succ =&gt; zero;
let oneInt: natGroup(int) = zero =&gt; succ =&gt; succ (zero);
let twoInt: natGroup(int) = zero =&gt; succ =&gt; succ (succ (zero));

--- 

zeroInt(zero, succ); oneInt(zero, succ); twoInt(zero, succ);

---

module Nat = {
  type t = int;
  
  let zero: t = 0;
  let succ: t =&gt; t = x =&gt; x + 1;
}

---

Nat.(zero); Nat.(succ(zero)); Nat.(succ(succ(zero)));

---

module type NatGroup = {
  type t;
  
  let zero: t;
  let succ: t =&gt; t;
};

---

module NatPriv: NatGroup = {
  include Nat; 
  let aPrivateMethod = () =&gt; (); // This stays within the module.
};

---

module type ShowNatGroup = {
  include NatGroup;
  let toString: t =&gt; string;
}

---

module ShowNat: ShowNatGroup = {
  include Nat;
  
  let toString = n =&gt; n == zero ? &quot;IsZero&quot; : &quot;IsNotZero&quot;; 
}

---

ShowNat.(zero); ShowNat.(succ(zero)); ShowNat.(succ(succ(zero)));

---

ShowNat.(toString(zero)); ShowNat.(toString(succ(zero)));

---

module type Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let printUntil: int =&gt; unit;
};

---

module Nat: Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let rec getItem = fun
    | 0 =&gt; ShowNatGroup.zero
    | i =&gt; ShowNatGroup.succ(getItem(i - 1));
  
  let printItem = item =&gt; print_endline(ShowNatGroup.toString(item));
  
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? ShowNatGroup.toString(item) : acc ++ &quot;, &quot; ++ ShowNatGroup.toString(item);
  
  let printUntil = n =&gt; {
    let items = List.init(n, getItem);
    print_endline(List.fold_left(join, &quot;&quot;, items));
  };
};

---

module NatInt = Nat({
  type t = int;
  let zero = 0;
  let succ = t =&gt; t + 1;
  let toString = string_of_int;
});

---

module NatBool = Nat({
  type t = bool;
  let zero = false;
  let succ = _ =&gt; true;
  let toString = string_of_bool;
});

---

module NatTern = Nat({
  type t = option(bool);
  let zero = Some(false);
  let succ = fun
    | Some(false) =&gt; None
    | _ =&gt; Some(true);
  let toString = fun
    | Some(item) =&gt; string_of_bool(item)
    | None =&gt; &quot;null&quot;;
});

---

NatBool.printUntil(3);
NatTern.printUntil(3);
NatInt.printUntil(3);

---

module NatChurch = {
  // Here&#x27;s where we get a bit creative with how we combine our Nats.
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? item : item ++ &quot; (&quot; ++ acc ++ &quot;)&quot;;

  // Extending the Nat functor for a specialized case. This is where ReasonML&#x27;s flexibility really shines.
  include Nat({
    type t = list(string);
    let zero = [];
    let succ = t =&gt; [&quot;f&quot;, ...t];
    let toString = t =&gt; List.fold_left(join, &quot;x&quot;, t);
  });
}

---

NatChurch.printUntil(3); 

nat1.re

type natGroup(&#x27;t) = &#x27;t =&gt; (&#x27;t =&gt; &#x27;t) =&gt; &#x27;t;
// type natGroup(&#x27;t) = (&#x27;t, &#x27;t =&gt; &#x27;t) =&gt; &#x27;t;

nat10.re

ShowNat.(zero); ShowNat.(succ(zero)); ShowNat.(succ(succ(zero)));
// - : ShowNat.t = &lt;abstr&gt;
// - : ShowNat.t = &lt;abstr&gt;
// - : ShowNat.t = &lt;abstr&gt;

nat10Real.re

module ShowNat: ShowNatGroup = {
  include Nat;
  
  let toString = n =&gt; n == zero ? &quot;IsZero&quot; : &quot;IsNotZero&quot;; 
}
// module ShowNat: ShowNatGroup;

nat11.re

ShowNat.(toString(zero)); ShowNat.(toString(succ(zero)));
// - : string = &quot;IsZero&quot;
// - : string = &quot;IsNotZero&quot;

nat12.re

module type Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let printUntil: int =&gt; unit;
};
/*
module type Nat =
  (ShowNatGroup : ShowNatGroup) =&gt; { let printUntil: int =&gt; unit; };
*/

nat13.re

module Nat: Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let rec getItem = fun
    | 0 =&gt; ShowNatGroup.zero
    | i =&gt; ShowNatGroup.succ(getItem(i - 1));
  
  let printItem = item =&gt; print_endline(ShowNatGroup.toString(item));
  
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? ShowNatGroup.toString(item) : acc ++ &quot;, &quot; ++ ShowNatGroup.toString(item);
  
  let printUntil = n =&gt; {
    let items = List.init(n, getItem);
    print_endline(List.fold_left(join, &quot;&quot;, items));
  };
};
// module Nat: Nat;

nat14.re

module NatInt = Nat({
  type t = int;
  let zero = 0;
  let succ = t =&gt; t + 1;
  let toString = string_of_int;
});
// module NatInt: { let printUntil: int =&gt; unit; };

nat15.re

module NatBool = Nat({
  type t = bool;
  let zero = false;
  let succ = _ =&gt; true;
  let toString = string_of_bool;
});
// module NatBool: { let printUntil: int =&gt; unit; };

nat16.re

module NatTern = Nat({
  type t = option(bool);
  let zero = Some(false);
  let succ = fun
    | Some(false) =&gt; None
    | _ =&gt; Some(true);
  let toString = fun
    | Some(item) =&gt; string_of_bool(item)
    | None =&gt; &quot;null&quot;;
});
// module NatTern: { let printUntil: int =&gt; unit; };

nat17.re

NatBool.printUntil(3);
// false, true, true

NatTern.printUntil(3);
// false, null, true

NatInt.printUntil(3);
// 0, 1, 2

nat18.re

module NatChurch = {
  // Here&#x27;s where we get a bit creative with how we combine our Nats.
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? item : item ++ &quot; (&quot; ++ acc ++ &quot;)&quot;;

  // Extending the Nat functor for a specialized case. This is where ReasonML&#x27;s flexibility really shines.
  include Nat({
    type t = list(string);
    let zero = [];
    let succ = t =&gt; [&quot;f&quot;, ...t];
    let toString = t =&gt; List.fold_left(join, &quot;x&quot;, t);
  });
}
/* 
module NatChurch:
  { let join: (string, string) =&gt; string; let printUntil: int =&gt; unit; };
*/

nat19.re

NatChurch.printUntil(3);
// x, f (x), f (f (x))

nat2.re

let zero: int = 0;
// let zero: int = 0;

let succ: int =&gt; int = x =&gt; x + 1;
// let succ: int =&gt; int = &lt;fun&gt;;

nat3.re

let zeroInt: natGroup(int) = zero =&gt; succ =&gt; zero;
// let zeroInt: natGroup(int) = &lt;fun&gt;;

let oneInt: natGroup(int) = zero =&gt; succ =&gt; succ (zero);
// let oneInt: natGroup(int) = &lt;fun&gt;;

let twoInt: natGroup(int) = zero =&gt; succ =&gt; succ (succ (zero));
// let twoInt: natGroup(int) = &lt;fun&gt;;

nat4.re

zeroInt(zero, succ); oneInt(zero, succ); twoInt(zero, succ);
// - : int = 0
// - : int = 1
// - : int = 2

nat5.re

module Nat = {
  type t = int;
  
  let zero: t = 0;
  let succ: t =&gt; t = x =&gt; x + 1;
}
// module Nat: { type t = int; let zero: t; let succ: t =&gt; t; };

nat6.re

Nat.(zero); Nat.(succ(zero)); Nat.(succ(succ(zero)));
// - : Nat.t = 0
// - : Nat.t = 1
// - : Nat.t = 2

nat7.re

module type NatGroup = {
  type t;
  
  let zero: t;
  let succ: t =&gt; t;
};
// module type NatGroup = { type t; let zero: t; let succ: t =&gt; t; };

nat8.re

module NatPriv: NatGroup = {
  include Nat; 
  let aPrivateMethod = () =&gt; (); // This stays within the module.
};
// module NatPriv: NatGroup;

nat9.re

module type ShowNatGroup = {
  include NatGroup;
  let toString: t =&gt; string;
}
/* 
module type ShowNatGroup =
  { type t; let zero: t; let succ: t =&gt; t; let toString: t =&gt; string; };
*/</code></pre><p>Running <code>NatChurch.printUntil(3)</code> showcases how you can adapt and extend functionality in a modular fashion, tailoring it to specific needs.</p><pre><code>nat.re

type natGroup(&#x27;t) = &#x27;t =&gt; (&#x27;t =&gt; &#x27;t) =&gt; &#x27;t;

---

let zero: int = 0;
let succ: int =&gt; int = x =&gt; x + 1;

---

let zeroInt: natGroup(int) = zero =&gt; succ =&gt; zero;
let oneInt: natGroup(int) = zero =&gt; succ =&gt; succ (zero);
let twoInt: natGroup(int) = zero =&gt; succ =&gt; succ (succ (zero));

--- 

zeroInt(zero, succ); oneInt(zero, succ); twoInt(zero, succ);

---

module Nat = {
  type t = int;
  
  let zero: t = 0;
  let succ: t =&gt; t = x =&gt; x + 1;
}

---

Nat.(zero); Nat.(succ(zero)); Nat.(succ(succ(zero)));

---

module type NatGroup = {
  type t;
  
  let zero: t;
  let succ: t =&gt; t;
};

---

module NatPriv: NatGroup = {
  include Nat; 
  let aPrivateMethod = () =&gt; (); // This stays within the module.
};

---

module type ShowNatGroup = {
  include NatGroup;
  let toString: t =&gt; string;
}

---

module ShowNat: ShowNatGroup = {
  include Nat;
  
  let toString = n =&gt; n == zero ? &quot;IsZero&quot; : &quot;IsNotZero&quot;; 
}

---

ShowNat.(zero); ShowNat.(succ(zero)); ShowNat.(succ(succ(zero)));

---

ShowNat.(toString(zero)); ShowNat.(toString(succ(zero)));

---

module type Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let printUntil: int =&gt; unit;
};

---

module Nat: Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let rec getItem = fun
    | 0 =&gt; ShowNatGroup.zero
    | i =&gt; ShowNatGroup.succ(getItem(i - 1));
  
  let printItem = item =&gt; print_endline(ShowNatGroup.toString(item));
  
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? ShowNatGroup.toString(item) : acc ++ &quot;, &quot; ++ ShowNatGroup.toString(item);
  
  let printUntil = n =&gt; {
    let items = List.init(n, getItem);
    print_endline(List.fold_left(join, &quot;&quot;, items));
  };
};

---

module NatInt = Nat({
  type t = int;
  let zero = 0;
  let succ = t =&gt; t + 1;
  let toString = string_of_int;
});

---

module NatBool = Nat({
  type t = bool;
  let zero = false;
  let succ = _ =&gt; true;
  let toString = string_of_bool;
});

---

module NatTern = Nat({
  type t = option(bool);
  let zero = Some(false);
  let succ = fun
    | Some(false) =&gt; None
    | _ =&gt; Some(true);
  let toString = fun
    | Some(item) =&gt; string_of_bool(item)
    | None =&gt; &quot;null&quot;;
});

---

NatBool.printUntil(3);
NatTern.printUntil(3);
NatInt.printUntil(3);

---

module NatChurch = {
  // Here&#x27;s where we get a bit creative with how we combine our Nats.
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? item : item ++ &quot; (&quot; ++ acc ++ &quot;)&quot;;

  // Extending the Nat functor for a specialized case. This is where ReasonML&#x27;s flexibility really shines.
  include Nat({
    type t = list(string);
    let zero = [];
    let succ = t =&gt; [&quot;f&quot;, ...t];
    let toString = t =&gt; List.fold_left(join, &quot;x&quot;, t);
  });
}

---

NatChurch.printUntil(3); 

nat1.re

type natGroup(&#x27;t) = &#x27;t =&gt; (&#x27;t =&gt; &#x27;t) =&gt; &#x27;t;
// type natGroup(&#x27;t) = (&#x27;t, &#x27;t =&gt; &#x27;t) =&gt; &#x27;t;

nat10.re

ShowNat.(zero); ShowNat.(succ(zero)); ShowNat.(succ(succ(zero)));
// - : ShowNat.t = &lt;abstr&gt;
// - : ShowNat.t = &lt;abstr&gt;
// - : ShowNat.t = &lt;abstr&gt;

nat10Real.re

module ShowNat: ShowNatGroup = {
  include Nat;
  
  let toString = n =&gt; n == zero ? &quot;IsZero&quot; : &quot;IsNotZero&quot;; 
}
// module ShowNat: ShowNatGroup;

nat11.re

ShowNat.(toString(zero)); ShowNat.(toString(succ(zero)));
// - : string = &quot;IsZero&quot;
// - : string = &quot;IsNotZero&quot;

nat12.re

module type Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let printUntil: int =&gt; unit;
};
/*
module type Nat =
  (ShowNatGroup : ShowNatGroup) =&gt; { let printUntil: int =&gt; unit; };
*/

nat13.re

module Nat: Nat = (ShowNatGroup: ShowNatGroup) =&gt; {
  let rec getItem = fun
    | 0 =&gt; ShowNatGroup.zero
    | i =&gt; ShowNatGroup.succ(getItem(i - 1));
  
  let printItem = item =&gt; print_endline(ShowNatGroup.toString(item));
  
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? ShowNatGroup.toString(item) : acc ++ &quot;, &quot; ++ ShowNatGroup.toString(item);
  
  let printUntil = n =&gt; {
    let items = List.init(n, getItem);
    print_endline(List.fold_left(join, &quot;&quot;, items));
  };
};
// module Nat: Nat;

nat14.re

module NatInt = Nat({
  type t = int;
  let zero = 0;
  let succ = t =&gt; t + 1;
  let toString = string_of_int;
});
// module NatInt: { let printUntil: int =&gt; unit; };

nat15.re

module NatBool = Nat({
  type t = bool;
  let zero = false;
  let succ = _ =&gt; true;
  let toString = string_of_bool;
});
// module NatBool: { let printUntil: int =&gt; unit; };

nat16.re

module NatTern = Nat({
  type t = option(bool);
  let zero = Some(false);
  let succ = fun
    | Some(false) =&gt; None
    | _ =&gt; Some(true);
  let toString = fun
    | Some(item) =&gt; string_of_bool(item)
    | None =&gt; &quot;null&quot;;
});
// module NatTern: { let printUntil: int =&gt; unit; };

nat17.re

NatBool.printUntil(3);
// false, true, true

NatTern.printUntil(3);
// false, null, true

NatInt.printUntil(3);
// 0, 1, 2

nat18.re

module NatChurch = {
  // Here&#x27;s where we get a bit creative with how we combine our Nats.
  let join = acc =&gt; item =&gt; acc == &quot;&quot; ? item : item ++ &quot; (&quot; ++ acc ++ &quot;)&quot;;

  // Extending the Nat functor for a specialized case. This is where ReasonML&#x27;s flexibility really shines.
  include Nat({
    type t = list(string);
    let zero = [];
    let succ = t =&gt; [&quot;f&quot;, ...t];
    let toString = t =&gt; List.fold_left(join, &quot;x&quot;, t);
  });
}
/* 
module NatChurch:
  { let join: (string, string) =&gt; string; let printUntil: int =&gt; unit; };
*/

nat19.re

NatChurch.printUntil(3);
// x, f (x), f (f (x))

nat2.re

let zero: int = 0;
// let zero: int = 0;

let succ: int =&gt; int = x =&gt; x + 1;
// let succ: int =&gt; int = &lt;fun&gt;;

nat3.re

let zeroInt: natGroup(int) = zero =&gt; succ =&gt; zero;
// let zeroInt: natGroup(int) = &lt;fun&gt;;

let oneInt: natGroup(int) = zero =&gt; succ =&gt; succ (zero);
// let oneInt: natGroup(int) = &lt;fun&gt;;

let twoInt: natGroup(int) = zero =&gt; succ =&gt; succ (succ (zero));
// let twoInt: natGroup(int) = &lt;fun&gt;;

nat4.re

zeroInt(zero, succ); oneInt(zero, succ); twoInt(zero, succ);
// - : int = 0
// - : int = 1
// - : int = 2

nat5.re

module Nat = {
  type t = int;
  
  let zero: t = 0;
  let succ: t =&gt; t = x =&gt; x + 1;
}
// module Nat: { type t = int; let zero: t; let succ: t =&gt; t; };

nat6.re

Nat.(zero); Nat.(succ(zero)); Nat.(succ(succ(zero)));
// - : Nat.t = 0
// - : Nat.t = 1
// - : Nat.t = 2

nat7.re

module type NatGroup = {
  type t;
  
  let zero: t;
  let succ: t =&gt; t;
};
// module type NatGroup = { type t; let zero: t; let succ: t =&gt; t; };

nat8.re

module NatPriv: NatGroup = {
  include Nat; 
  let aPrivateMethod = () =&gt; (); // This stays within the module.
};
// module NatPriv: NatGroup;

nat9.re

module type ShowNatGroup = {
  include NatGroup;
  let toString: t =&gt; string;
}
/* 
module type ShowNatGroup =
  { type t; let zero: t; let succ: t =&gt; t; let toString: t =&gt; string; };
*/</code></pre><p>This exploration through ReasonML’s type system, modules, and functors is more than just a magic trick. It’s about finding practical, elegant solutions to complex problems. Leveraging these features, you can design code that’s not only efficient and scalable but also clear and maintainable. ReasonML encourages a thoughtful approach to software design, where every line of code serves a purpose, and every module fits neatly into the larger puzzle.</p><p>The next use case will be a perfect final for the series, so stay tuned!</p><p>For quick navigation, here are the other articles in the same series:</p><p><a href="https://yamaceay.medium.com/learn-with-me-reasonml-part-1-83b48d9ef694">Learn With Me: ReasonML, Part 1</a></p><p><a href="https://yamaceay.medium.com/learn-with-me-reasonml-part-3-fa246cc034f1">Learn With Me: ReasonML, Part 3</a></p>
