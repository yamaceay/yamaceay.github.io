---
layout: post
title: "Learn With Me: ReasonML, Part 1"
date: 2024-03-26T22:30:29+00:00
original_url: "https://medium.com/@yamaceay/learn-with-me-reasonml-part-1-83b48d9ef694"
tags: []
excerpt: "Source: String (computer science), Wikipedia This article requires you to have a basic understanding of ReasonML, a functional programming language which I partly covered in one of my previous article"
---

<figure><img alt="" src="https://cdn-images-1.medium.com/max/1400/1*r6T1vqEVQr3oitLPCx_biQ.png" /><figcaption>Source: String (computer science), Wikipedia</figcaption></figure><p>This article requires you to have a basic understanding of ReasonML, a functional programming language which I partly covered in one of my previous articles.</p><p><a href="https://yamaceay.medium.com/how-to-learn-a-coding-language-fast-ad7a99eaf375">How to Learn a Coding Language (Fast)</a></p><p>For quick navigation, here are the other articles in the same series:</p><p><a href="https://yamaceay.medium.com/learn-with-me-reasonml-part-2-6f704e0ded0b">Learn With Me: ReasonML, Part 2</a></p><p><a href="https://yamaceay.medium.com/learn-with-me-reasonml-part-3-fa246cc034f1">Learn With Me: ReasonML, Part 3</a></p><p>Without further ado, let’s just dive into implementing a safe split method for strings. It’s a common task, but with a twist to make it interesting.</p><p>Starting off with a test case, because examples light the way: Splitting <code>a_b,c_d,e_f</code> by <code>,</code> should give us <code>[&quot;a_b&quot;,&quot;c_d&quot;,&quot;e_f”]</code>,<br/>and by <code>_</code> we get <code>[&quot;a&quot;,&quot;b,c&quot;,&quot;d_e&quot;,&quot;f”]</code>. A neat little setup to see our function in action.</p><pre><code>Whole Split

split.re

let joinedStr = &quot;a_b,c_d,e_f&quot;;
// let joinedStr: string = &quot;a_b,c_d,e_f&quot;;

String.split_on_char(&#x27;,&#x27;, joinedStr);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

String.split_on_char(&#x27;_&#x27;, joinedStr);
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]


---

let splitReal = (str: string, delim: char, take: int) =&gt; {
  let values = String.split_on_char(delim, str);
  let len = List.length(values);
  
  // Keeping &#x27;take&#x27; within reasonable bounds was crucial. 
  if (take &gt; len) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &gt; &quot; ++ string_of_int(len) ++ &quot; (length)&quot;));
  };
  
  if (take &lt; -1) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &lt; -1 (wildcard)&quot;));
  };
  
  // Deciding on the exact number of pieces to take felt like balancing equations.
  let takeMod = if (take == -1) { // The wildcard case for all items.
    len &gt; 0 ? len - 1 : -1;
  } else { // Or just a specific count.
    len &gt; 0 &amp;&amp; take &gt; 0 ? (take - 1) mod len : -1;
  };
  
  // From there, it was about picking the right slices.
  let filteredValues = ref([]);
  for (i in 0 to takeMod) {
    filteredValues := List.append(filteredValues^, [List.nth(values, i)]);
  };
  filteredValues^;
}
// let splitReal: (string, char, int) =&gt; list(string) = &lt;fun&gt;;


---

splitReal(joinedStr, &#x27;,&#x27;, -1);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

---

let split = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = -1, ()) =&gt; {
  splitReal(str, delim, take);
};
// let split: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;


---

split(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

split(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]


---

for (i in -3 to List.length(split(joinedStr, ())) + 2) {
  let (result, suffix) = try((split(joinedStr, ~take=i, ()), &quot;&quot;)) {
    | Invalid_argument(msg) =&gt; ([], &quot;Invalid argument: &quot; ++ msg)
  };
  
  let resultString = List.fold_left((acc, item) =&gt; acc == &quot;&quot; ? item : acc ++ &quot; &quot; ++ item, &quot;&quot;, result);
  print_endline(&quot;-- take: &quot; ++ string_of_int(i) ++ &quot;, result: &quot; ++ resultString ++ suffix);
};
/*
-- take: -3, result: Invalid argument: -3 &lt; -1 (wildcard)
-- take: -2, result: Invalid argument: -2 &lt; -1 (wildcard)
-- take: -1, result: a_b c_d e_f
-- take: 0, result: 
-- take: 1, result: a_b
-- take: 2, result: a_b c_d
-- take: 3, result: a_b c_d e_f
-- take: 4, result: Invalid argument: 4 &gt; 3 (length)
-- take: 5, result: Invalid argument: 5 &gt; 3 (length)
*/

---

split(&quot;&quot;, ());
// - : list(string) = [&quot;&quot;]


---

let splitSafe = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = str == &quot;&quot; ? 0 : -1, ()) =&gt; {
  split(str, ~delim=delim, ~take=take, ());
};
// let splitSafe: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

---

splitSafe(&quot;&quot;, ());
// - : list(string) = []


--- 

let splitSafer = (str: string, ~delim: option(char) = ?, ~take: option(int) = ?, ()) =&gt; {
  // This bit of logic ensures we&#x27;re always using sensible defaults.
  let newDelim = switch(delim) {
    | None =&gt; &#x27;,&#x27;
    | Some(value) =&gt; value
  };
  
  let newTake = switch(take) {
    | None =&gt; str == &quot;&quot; ? 0 : -1
    | Some(value) =&gt; value
  };

  // With these adjustments, we&#x27;re all set to make the split function even more user-friendly.
  split(str, ~delim=newDelim, ~take=newTake, ());
};
// let splitSafer: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;


--- 

splitSafer(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=?None, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

splitSafer(joinedStr, ~delim=?Some(&#x27;_&#x27;), ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split1.re

let joinedStr = &quot;a_b,c_d,e_f&quot;;
// let joinedStr: string = &quot;a_b,c_d,e_f&quot;;

String.split_on_char(&#x27;,&#x27;, joinedStr);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

String.split_on_char(&#x27;_&#x27;, joinedStr);
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split10.re

let splitSafer = (str: string, ~delim: option(char) = ?, ~take: option(int) = ?, ()) =&gt; {
  // This bit of logic ensures we&#x27;re always using sensible defaults.
  let newDelim = switch(delim) {
    | None =&gt; &#x27;,&#x27;
    | Some(value) =&gt; value
  };
  
  let newTake = switch(take) {
    | None =&gt; str == &quot;&quot; ? 0 : -1
    | Some(value) =&gt; value
  };

  // With these adjustments, we&#x27;re all set to make the split function even more user-friendly.
  split(str, ~delim=newDelim, ~take=newTake, ());
};
// let splitSafer: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

split11.re

splitSafer(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=?None, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

splitSafer(joinedStr, ~delim=?Some(&#x27;_&#x27;), ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split2.re

let splitReal = (str: string, delim: char, take: int) =&gt; {
  let values = String.split_on_char(delim, str);
  let len = List.length(values);
  
  // Keeping &#x27;take&#x27; within reasonable bounds was crucial. 
  if (take &gt; len) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &gt; &quot; ++ string_of_int(len) ++ &quot; (length)&quot;));
  };
  
  if (take &lt; -1) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &lt; -1 (wildcard)&quot;));
  };
  
  // Deciding on the exact number of pieces to take felt like balancing equations.
  let takeMod = if (take == -1) { // The wildcard case for all items.
    len &gt; 0 ? len - 1 : -1;
  } else { // Or just a specific count.
    len &gt; 0 &amp;&amp; take &gt; 0 ? (take - 1) mod len : -1;
  };
  
  // From there, it was about picking the right slices.
  let filteredValues = ref([]);
  for (i in 0 to takeMod) {
    filteredValues := List.append(filteredValues^, [List.nth(values, i)]);
  };
  filteredValues^;
}
// let splitReal: (string, char, int) =&gt; list(string) = &lt;fun&gt;;

split3.re

splitReal(joinedStr, &#x27;,&#x27;, -1);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

split4.re

let split = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = -1, ()) =&gt; {
  splitReal(str, delim, take);
};
// let split: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

split5.re

split(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

split(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split6.re

for (i in -3 to List.length(split(joinedStr, ())) + 2) {
  let (result, suffix) = try((split(joinedStr, ~take=i, ()), &quot;&quot;)) {
    | Invalid_argument(msg) =&gt; ([], &quot;Invalid argument: &quot; ++ msg)
  };
  
  let resultString = List.fold_left((acc, item) =&gt; acc == &quot;&quot; ? item : acc ++ &quot; &quot; ++ item, &quot;&quot;, result);
  print_endline(&quot;-- take: &quot; ++ string_of_int(i) ++ &quot;, result: &quot; ++ resultString ++ suffix);
};
/*
-- take: -3, result: Invalid argument: -3 &lt; -1 (wildcard)
-- take: -2, result: Invalid argument: -2 &lt; -1 (wildcard)
-- take: -1, result: a_b c_d e_f
-- take: 0, result: 
-- take: 1, result: a_b
-- take: 2, result: a_b c_d
-- take: 3, result: a_b c_d e_f
-- take: 4, result: Invalid argument: 4 &gt; 3 (length)
-- take: 5, result: Invalid argument: 5 &gt; 3 (length)
*/

split7.re

split(&quot;&quot;, ());
// - : list(string) = [&quot;&quot;]

split8.re

let splitSafe = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = str == &quot;&quot; ? 0 : -1, ()) =&gt; {
  split(str, ~delim=delim, ~take=take, ());
};
// let splitSafe: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

split9.re

splitSafe(&quot;&quot;, ());
// - : list(string) = []</code></pre><p>Here’s my take on the first implementation. It’s got a few parameters:</p><ul><li>str: the string we’re splitting.</li><li>delim: a delimiter, with a default preference for comma (,).</li><li>take: how many pieces we want, where -1 means “give us everything”</li></ul><pre><code>Whole Split

split.re

let joinedStr = &quot;a_b,c_d,e_f&quot;;
// let joinedStr: string = &quot;a_b,c_d,e_f&quot;;

String.split_on_char(&#x27;,&#x27;, joinedStr);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

String.split_on_char(&#x27;_&#x27;, joinedStr);
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]


---

let splitReal = (str: string, delim: char, take: int) =&gt; {
  let values = String.split_on_char(delim, str);
  let len = List.length(values);
  
  // Keeping &#x27;take&#x27; within reasonable bounds was crucial. 
  if (take &gt; len) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &gt; &quot; ++ string_of_int(len) ++ &quot; (length)&quot;));
  };
  
  if (take &lt; -1) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &lt; -1 (wildcard)&quot;));
  };
  
  // Deciding on the exact number of pieces to take felt like balancing equations.
  let takeMod = if (take == -1) { // The wildcard case for all items.
    len &gt; 0 ? len - 1 : -1;
  } else { // Or just a specific count.
    len &gt; 0 &amp;&amp; take &gt; 0 ? (take - 1) mod len : -1;
  };
  
  // From there, it was about picking the right slices.
  let filteredValues = ref([]);
  for (i in 0 to takeMod) {
    filteredValues := List.append(filteredValues^, [List.nth(values, i)]);
  };
  filteredValues^;
}
// let splitReal: (string, char, int) =&gt; list(string) = &lt;fun&gt;;


---

splitReal(joinedStr, &#x27;,&#x27;, -1);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

---

let split = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = -1, ()) =&gt; {
  splitReal(str, delim, take);
};
// let split: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;


---

split(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

split(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]


---

for (i in -3 to List.length(split(joinedStr, ())) + 2) {
  let (result, suffix) = try((split(joinedStr, ~take=i, ()), &quot;&quot;)) {
    | Invalid_argument(msg) =&gt; ([], &quot;Invalid argument: &quot; ++ msg)
  };
  
  let resultString = List.fold_left((acc, item) =&gt; acc == &quot;&quot; ? item : acc ++ &quot; &quot; ++ item, &quot;&quot;, result);
  print_endline(&quot;-- take: &quot; ++ string_of_int(i) ++ &quot;, result: &quot; ++ resultString ++ suffix);
};
/*
-- take: -3, result: Invalid argument: -3 &lt; -1 (wildcard)
-- take: -2, result: Invalid argument: -2 &lt; -1 (wildcard)
-- take: -1, result: a_b c_d e_f
-- take: 0, result: 
-- take: 1, result: a_b
-- take: 2, result: a_b c_d
-- take: 3, result: a_b c_d e_f
-- take: 4, result: Invalid argument: 4 &gt; 3 (length)
-- take: 5, result: Invalid argument: 5 &gt; 3 (length)
*/

---

split(&quot;&quot;, ());
// - : list(string) = [&quot;&quot;]


---

let splitSafe = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = str == &quot;&quot; ? 0 : -1, ()) =&gt; {
  split(str, ~delim=delim, ~take=take, ());
};
// let splitSafe: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

---

splitSafe(&quot;&quot;, ());
// - : list(string) = []


--- 

let splitSafer = (str: string, ~delim: option(char) = ?, ~take: option(int) = ?, ()) =&gt; {
  // This bit of logic ensures we&#x27;re always using sensible defaults.
  let newDelim = switch(delim) {
    | None =&gt; &#x27;,&#x27;
    | Some(value) =&gt; value
  };
  
  let newTake = switch(take) {
    | None =&gt; str == &quot;&quot; ? 0 : -1
    | Some(value) =&gt; value
  };

  // With these adjustments, we&#x27;re all set to make the split function even more user-friendly.
  split(str, ~delim=newDelim, ~take=newTake, ());
};
// let splitSafer: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;


--- 

splitSafer(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=?None, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

splitSafer(joinedStr, ~delim=?Some(&#x27;_&#x27;), ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split1.re

let joinedStr = &quot;a_b,c_d,e_f&quot;;
// let joinedStr: string = &quot;a_b,c_d,e_f&quot;;

String.split_on_char(&#x27;,&#x27;, joinedStr);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

String.split_on_char(&#x27;_&#x27;, joinedStr);
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split10.re

let splitSafer = (str: string, ~delim: option(char) = ?, ~take: option(int) = ?, ()) =&gt; {
  // This bit of logic ensures we&#x27;re always using sensible defaults.
  let newDelim = switch(delim) {
    | None =&gt; &#x27;,&#x27;
    | Some(value) =&gt; value
  };
  
  let newTake = switch(take) {
    | None =&gt; str == &quot;&quot; ? 0 : -1
    | Some(value) =&gt; value
  };

  // With these adjustments, we&#x27;re all set to make the split function even more user-friendly.
  split(str, ~delim=newDelim, ~take=newTake, ());
};
// let splitSafer: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

split11.re

splitSafer(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=?None, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

splitSafer(joinedStr, ~delim=?Some(&#x27;_&#x27;), ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split2.re

let splitReal = (str: string, delim: char, take: int) =&gt; {
  let values = String.split_on_char(delim, str);
  let len = List.length(values);
  
  // Keeping &#x27;take&#x27; within reasonable bounds was crucial. 
  if (take &gt; len) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &gt; &quot; ++ string_of_int(len) ++ &quot; (length)&quot;));
  };
  
  if (take &lt; -1) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &lt; -1 (wildcard)&quot;));
  };
  
  // Deciding on the exact number of pieces to take felt like balancing equations.
  let takeMod = if (take == -1) { // The wildcard case for all items.
    len &gt; 0 ? len - 1 : -1;
  } else { // Or just a specific count.
    len &gt; 0 &amp;&amp; take &gt; 0 ? (take - 1) mod len : -1;
  };
  
  // From there, it was about picking the right slices.
  let filteredValues = ref([]);
  for (i in 0 to takeMod) {
    filteredValues := List.append(filteredValues^, [List.nth(values, i)]);
  };
  filteredValues^;
}
// let splitReal: (string, char, int) =&gt; list(string) = &lt;fun&gt;;

split3.re

splitReal(joinedStr, &#x27;,&#x27;, -1);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

split4.re

let split = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = -1, ()) =&gt; {
  splitReal(str, delim, take);
};
// let split: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

split5.re

split(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

split(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split6.re

for (i in -3 to List.length(split(joinedStr, ())) + 2) {
  let (result, suffix) = try((split(joinedStr, ~take=i, ()), &quot;&quot;)) {
    | Invalid_argument(msg) =&gt; ([], &quot;Invalid argument: &quot; ++ msg)
  };
  
  let resultString = List.fold_left((acc, item) =&gt; acc == &quot;&quot; ? item : acc ++ &quot; &quot; ++ item, &quot;&quot;, result);
  print_endline(&quot;-- take: &quot; ++ string_of_int(i) ++ &quot;, result: &quot; ++ resultString ++ suffix);
};
/*
-- take: -3, result: Invalid argument: -3 &lt; -1 (wildcard)
-- take: -2, result: Invalid argument: -2 &lt; -1 (wildcard)
-- take: -1, result: a_b c_d e_f
-- take: 0, result: 
-- take: 1, result: a_b
-- take: 2, result: a_b c_d
-- take: 3, result: a_b c_d e_f
-- take: 4, result: Invalid argument: 4 &gt; 3 (length)
-- take: 5, result: Invalid argument: 5 &gt; 3 (length)
*/

split7.re

split(&quot;&quot;, ());
// - : list(string) = [&quot;&quot;]

split8.re

let splitSafe = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = str == &quot;&quot; ? 0 : -1, ()) =&gt; {
  split(str, ~delim=delim, ~take=take, ());
};
// let splitSafe: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

split9.re

splitSafe(&quot;&quot;, ());
// - : list(string) = []</code></pre><p>After some time, I realized that some arguments like the common “comma” delimiter don’t really change much.<br/>So, why not make them defaults to simplify our lives?</p><pre><code>Whole Split

split.re

let joinedStr = &quot;a_b,c_d,e_f&quot;;
// let joinedStr: string = &quot;a_b,c_d,e_f&quot;;

String.split_on_char(&#x27;,&#x27;, joinedStr);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

String.split_on_char(&#x27;_&#x27;, joinedStr);
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]


---

let splitReal = (str: string, delim: char, take: int) =&gt; {
  let values = String.split_on_char(delim, str);
  let len = List.length(values);
  
  // Keeping &#x27;take&#x27; within reasonable bounds was crucial. 
  if (take &gt; len) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &gt; &quot; ++ string_of_int(len) ++ &quot; (length)&quot;));
  };
  
  if (take &lt; -1) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &lt; -1 (wildcard)&quot;));
  };
  
  // Deciding on the exact number of pieces to take felt like balancing equations.
  let takeMod = if (take == -1) { // The wildcard case for all items.
    len &gt; 0 ? len - 1 : -1;
  } else { // Or just a specific count.
    len &gt; 0 &amp;&amp; take &gt; 0 ? (take - 1) mod len : -1;
  };
  
  // From there, it was about picking the right slices.
  let filteredValues = ref([]);
  for (i in 0 to takeMod) {
    filteredValues := List.append(filteredValues^, [List.nth(values, i)]);
  };
  filteredValues^;
}
// let splitReal: (string, char, int) =&gt; list(string) = &lt;fun&gt;;


---

splitReal(joinedStr, &#x27;,&#x27;, -1);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

---

let split = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = -1, ()) =&gt; {
  splitReal(str, delim, take);
};
// let split: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;


---

split(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

split(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]


---

for (i in -3 to List.length(split(joinedStr, ())) + 2) {
  let (result, suffix) = try((split(joinedStr, ~take=i, ()), &quot;&quot;)) {
    | Invalid_argument(msg) =&gt; ([], &quot;Invalid argument: &quot; ++ msg)
  };
  
  let resultString = List.fold_left((acc, item) =&gt; acc == &quot;&quot; ? item : acc ++ &quot; &quot; ++ item, &quot;&quot;, result);
  print_endline(&quot;-- take: &quot; ++ string_of_int(i) ++ &quot;, result: &quot; ++ resultString ++ suffix);
};
/*
-- take: -3, result: Invalid argument: -3 &lt; -1 (wildcard)
-- take: -2, result: Invalid argument: -2 &lt; -1 (wildcard)
-- take: -1, result: a_b c_d e_f
-- take: 0, result: 
-- take: 1, result: a_b
-- take: 2, result: a_b c_d
-- take: 3, result: a_b c_d e_f
-- take: 4, result: Invalid argument: 4 &gt; 3 (length)
-- take: 5, result: Invalid argument: 5 &gt; 3 (length)
*/

---

split(&quot;&quot;, ());
// - : list(string) = [&quot;&quot;]


---

let splitSafe = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = str == &quot;&quot; ? 0 : -1, ()) =&gt; {
  split(str, ~delim=delim, ~take=take, ());
};
// let splitSafe: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

---

splitSafe(&quot;&quot;, ());
// - : list(string) = []


--- 

let splitSafer = (str: string, ~delim: option(char) = ?, ~take: option(int) = ?, ()) =&gt; {
  // This bit of logic ensures we&#x27;re always using sensible defaults.
  let newDelim = switch(delim) {
    | None =&gt; &#x27;,&#x27;
    | Some(value) =&gt; value
  };
  
  let newTake = switch(take) {
    | None =&gt; str == &quot;&quot; ? 0 : -1
    | Some(value) =&gt; value
  };

  // With these adjustments, we&#x27;re all set to make the split function even more user-friendly.
  split(str, ~delim=newDelim, ~take=newTake, ());
};
// let splitSafer: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;


--- 

splitSafer(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=?None, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

splitSafer(joinedStr, ~delim=?Some(&#x27;_&#x27;), ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split1.re

let joinedStr = &quot;a_b,c_d,e_f&quot;;
// let joinedStr: string = &quot;a_b,c_d,e_f&quot;;

String.split_on_char(&#x27;,&#x27;, joinedStr);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

String.split_on_char(&#x27;_&#x27;, joinedStr);
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split10.re

let splitSafer = (str: string, ~delim: option(char) = ?, ~take: option(int) = ?, ()) =&gt; {
  // This bit of logic ensures we&#x27;re always using sensible defaults.
  let newDelim = switch(delim) {
    | None =&gt; &#x27;,&#x27;
    | Some(value) =&gt; value
  };
  
  let newTake = switch(take) {
    | None =&gt; str == &quot;&quot; ? 0 : -1
    | Some(value) =&gt; value
  };

  // With these adjustments, we&#x27;re all set to make the split function even more user-friendly.
  split(str, ~delim=newDelim, ~take=newTake, ());
};
// let splitSafer: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

split11.re

splitSafer(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=?None, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

splitSafer(joinedStr, ~delim=?Some(&#x27;_&#x27;), ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split2.re

let splitReal = (str: string, delim: char, take: int) =&gt; {
  let values = String.split_on_char(delim, str);
  let len = List.length(values);
  
  // Keeping &#x27;take&#x27; within reasonable bounds was crucial. 
  if (take &gt; len) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &gt; &quot; ++ string_of_int(len) ++ &quot; (length)&quot;));
  };
  
  if (take &lt; -1) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &lt; -1 (wildcard)&quot;));
  };
  
  // Deciding on the exact number of pieces to take felt like balancing equations.
  let takeMod = if (take == -1) { // The wildcard case for all items.
    len &gt; 0 ? len - 1 : -1;
  } else { // Or just a specific count.
    len &gt; 0 &amp;&amp; take &gt; 0 ? (take - 1) mod len : -1;
  };
  
  // From there, it was about picking the right slices.
  let filteredValues = ref([]);
  for (i in 0 to takeMod) {
    filteredValues := List.append(filteredValues^, [List.nth(values, i)]);
  };
  filteredValues^;
}
// let splitReal: (string, char, int) =&gt; list(string) = &lt;fun&gt;;

split3.re

splitReal(joinedStr, &#x27;,&#x27;, -1);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

split4.re

let split = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = -1, ()) =&gt; {
  splitReal(str, delim, take);
};
// let split: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

split5.re

split(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

split(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split6.re

for (i in -3 to List.length(split(joinedStr, ())) + 2) {
  let (result, suffix) = try((split(joinedStr, ~take=i, ()), &quot;&quot;)) {
    | Invalid_argument(msg) =&gt; ([], &quot;Invalid argument: &quot; ++ msg)
  };
  
  let resultString = List.fold_left((acc, item) =&gt; acc == &quot;&quot; ? item : acc ++ &quot; &quot; ++ item, &quot;&quot;, result);
  print_endline(&quot;-- take: &quot; ++ string_of_int(i) ++ &quot;, result: &quot; ++ resultString ++ suffix);
};
/*
-- take: -3, result: Invalid argument: -3 &lt; -1 (wildcard)
-- take: -2, result: Invalid argument: -2 &lt; -1 (wildcard)
-- take: -1, result: a_b c_d e_f
-- take: 0, result: 
-- take: 1, result: a_b
-- take: 2, result: a_b c_d
-- take: 3, result: a_b c_d e_f
-- take: 4, result: Invalid argument: 4 &gt; 3 (length)
-- take: 5, result: Invalid argument: 5 &gt; 3 (length)
*/

split7.re

split(&quot;&quot;, ());
// - : list(string) = [&quot;&quot;]

split8.re

let splitSafe = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = str == &quot;&quot; ? 0 : -1, ()) =&gt; {
  split(str, ~delim=delim, ~take=take, ());
};
// let splitSafe: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

split9.re

splitSafe(&quot;&quot;, ());
// - : list(string) = []</code></pre><p>That led me to introduce labeled arguments. It’s a small tweak but makes the function call much clearer.</p><pre><code>Whole Split

split.re

let joinedStr = &quot;a_b,c_d,e_f&quot;;
// let joinedStr: string = &quot;a_b,c_d,e_f&quot;;

String.split_on_char(&#x27;,&#x27;, joinedStr);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

String.split_on_char(&#x27;_&#x27;, joinedStr);
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]


---

let splitReal = (str: string, delim: char, take: int) =&gt; {
  let values = String.split_on_char(delim, str);
  let len = List.length(values);
  
  // Keeping &#x27;take&#x27; within reasonable bounds was crucial. 
  if (take &gt; len) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &gt; &quot; ++ string_of_int(len) ++ &quot; (length)&quot;));
  };
  
  if (take &lt; -1) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &lt; -1 (wildcard)&quot;));
  };
  
  // Deciding on the exact number of pieces to take felt like balancing equations.
  let takeMod = if (take == -1) { // The wildcard case for all items.
    len &gt; 0 ? len - 1 : -1;
  } else { // Or just a specific count.
    len &gt; 0 &amp;&amp; take &gt; 0 ? (take - 1) mod len : -1;
  };
  
  // From there, it was about picking the right slices.
  let filteredValues = ref([]);
  for (i in 0 to takeMod) {
    filteredValues := List.append(filteredValues^, [List.nth(values, i)]);
  };
  filteredValues^;
}
// let splitReal: (string, char, int) =&gt; list(string) = &lt;fun&gt;;


---

splitReal(joinedStr, &#x27;,&#x27;, -1);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

---

let split = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = -1, ()) =&gt; {
  splitReal(str, delim, take);
};
// let split: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;


---

split(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

split(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]


---

for (i in -3 to List.length(split(joinedStr, ())) + 2) {
  let (result, suffix) = try((split(joinedStr, ~take=i, ()), &quot;&quot;)) {
    | Invalid_argument(msg) =&gt; ([], &quot;Invalid argument: &quot; ++ msg)
  };
  
  let resultString = List.fold_left((acc, item) =&gt; acc == &quot;&quot; ? item : acc ++ &quot; &quot; ++ item, &quot;&quot;, result);
  print_endline(&quot;-- take: &quot; ++ string_of_int(i) ++ &quot;, result: &quot; ++ resultString ++ suffix);
};
/*
-- take: -3, result: Invalid argument: -3 &lt; -1 (wildcard)
-- take: -2, result: Invalid argument: -2 &lt; -1 (wildcard)
-- take: -1, result: a_b c_d e_f
-- take: 0, result: 
-- take: 1, result: a_b
-- take: 2, result: a_b c_d
-- take: 3, result: a_b c_d e_f
-- take: 4, result: Invalid argument: 4 &gt; 3 (length)
-- take: 5, result: Invalid argument: 5 &gt; 3 (length)
*/

---

split(&quot;&quot;, ());
// - : list(string) = [&quot;&quot;]


---

let splitSafe = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = str == &quot;&quot; ? 0 : -1, ()) =&gt; {
  split(str, ~delim=delim, ~take=take, ());
};
// let splitSafe: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

---

splitSafe(&quot;&quot;, ());
// - : list(string) = []


--- 

let splitSafer = (str: string, ~delim: option(char) = ?, ~take: option(int) = ?, ()) =&gt; {
  // This bit of logic ensures we&#x27;re always using sensible defaults.
  let newDelim = switch(delim) {
    | None =&gt; &#x27;,&#x27;
    | Some(value) =&gt; value
  };
  
  let newTake = switch(take) {
    | None =&gt; str == &quot;&quot; ? 0 : -1
    | Some(value) =&gt; value
  };

  // With these adjustments, we&#x27;re all set to make the split function even more user-friendly.
  split(str, ~delim=newDelim, ~take=newTake, ());
};
// let splitSafer: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;


--- 

splitSafer(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=?None, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

splitSafer(joinedStr, ~delim=?Some(&#x27;_&#x27;), ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split1.re

let joinedStr = &quot;a_b,c_d,e_f&quot;;
// let joinedStr: string = &quot;a_b,c_d,e_f&quot;;

String.split_on_char(&#x27;,&#x27;, joinedStr);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

String.split_on_char(&#x27;_&#x27;, joinedStr);
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split10.re

let splitSafer = (str: string, ~delim: option(char) = ?, ~take: option(int) = ?, ()) =&gt; {
  // This bit of logic ensures we&#x27;re always using sensible defaults.
  let newDelim = switch(delim) {
    | None =&gt; &#x27;,&#x27;
    | Some(value) =&gt; value
  };
  
  let newTake = switch(take) {
    | None =&gt; str == &quot;&quot; ? 0 : -1
    | Some(value) =&gt; value
  };

  // With these adjustments, we&#x27;re all set to make the split function even more user-friendly.
  split(str, ~delim=newDelim, ~take=newTake, ());
};
// let splitSafer: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

split11.re

splitSafer(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=?None, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

splitSafer(joinedStr, ~delim=?Some(&#x27;_&#x27;), ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split2.re

let splitReal = (str: string, delim: char, take: int) =&gt; {
  let values = String.split_on_char(delim, str);
  let len = List.length(values);
  
  // Keeping &#x27;take&#x27; within reasonable bounds was crucial. 
  if (take &gt; len) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &gt; &quot; ++ string_of_int(len) ++ &quot; (length)&quot;));
  };
  
  if (take &lt; -1) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &lt; -1 (wildcard)&quot;));
  };
  
  // Deciding on the exact number of pieces to take felt like balancing equations.
  let takeMod = if (take == -1) { // The wildcard case for all items.
    len &gt; 0 ? len - 1 : -1;
  } else { // Or just a specific count.
    len &gt; 0 &amp;&amp; take &gt; 0 ? (take - 1) mod len : -1;
  };
  
  // From there, it was about picking the right slices.
  let filteredValues = ref([]);
  for (i in 0 to takeMod) {
    filteredValues := List.append(filteredValues^, [List.nth(values, i)]);
  };
  filteredValues^;
}
// let splitReal: (string, char, int) =&gt; list(string) = &lt;fun&gt;;

split3.re

splitReal(joinedStr, &#x27;,&#x27;, -1);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

split4.re

let split = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = -1, ()) =&gt; {
  splitReal(str, delim, take);
};
// let split: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

split5.re

split(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

split(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split6.re

for (i in -3 to List.length(split(joinedStr, ())) + 2) {
  let (result, suffix) = try((split(joinedStr, ~take=i, ()), &quot;&quot;)) {
    | Invalid_argument(msg) =&gt; ([], &quot;Invalid argument: &quot; ++ msg)
  };
  
  let resultString = List.fold_left((acc, item) =&gt; acc == &quot;&quot; ? item : acc ++ &quot; &quot; ++ item, &quot;&quot;, result);
  print_endline(&quot;-- take: &quot; ++ string_of_int(i) ++ &quot;, result: &quot; ++ resultString ++ suffix);
};
/*
-- take: -3, result: Invalid argument: -3 &lt; -1 (wildcard)
-- take: -2, result: Invalid argument: -2 &lt; -1 (wildcard)
-- take: -1, result: a_b c_d e_f
-- take: 0, result: 
-- take: 1, result: a_b
-- take: 2, result: a_b c_d
-- take: 3, result: a_b c_d e_f
-- take: 4, result: Invalid argument: 4 &gt; 3 (length)
-- take: 5, result: Invalid argument: 5 &gt; 3 (length)
*/

split7.re

split(&quot;&quot;, ());
// - : list(string) = [&quot;&quot;]

split8.re

let splitSafe = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = str == &quot;&quot; ? 0 : -1, ()) =&gt; {
  split(str, ~delim=delim, ~take=take, ());
};
// let splitSafe: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

split9.re

splitSafe(&quot;&quot;, ());
// - : list(string) = []</code></pre><p>And here’s how you use it — simplicity in action.</p><pre><code>Whole Split

split.re

let joinedStr = &quot;a_b,c_d,e_f&quot;;
// let joinedStr: string = &quot;a_b,c_d,e_f&quot;;

String.split_on_char(&#x27;,&#x27;, joinedStr);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

String.split_on_char(&#x27;_&#x27;, joinedStr);
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]


---

let splitReal = (str: string, delim: char, take: int) =&gt; {
  let values = String.split_on_char(delim, str);
  let len = List.length(values);
  
  // Keeping &#x27;take&#x27; within reasonable bounds was crucial. 
  if (take &gt; len) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &gt; &quot; ++ string_of_int(len) ++ &quot; (length)&quot;));
  };
  
  if (take &lt; -1) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &lt; -1 (wildcard)&quot;));
  };
  
  // Deciding on the exact number of pieces to take felt like balancing equations.
  let takeMod = if (take == -1) { // The wildcard case for all items.
    len &gt; 0 ? len - 1 : -1;
  } else { // Or just a specific count.
    len &gt; 0 &amp;&amp; take &gt; 0 ? (take - 1) mod len : -1;
  };
  
  // From there, it was about picking the right slices.
  let filteredValues = ref([]);
  for (i in 0 to takeMod) {
    filteredValues := List.append(filteredValues^, [List.nth(values, i)]);
  };
  filteredValues^;
}
// let splitReal: (string, char, int) =&gt; list(string) = &lt;fun&gt;;


---

splitReal(joinedStr, &#x27;,&#x27;, -1);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

---

let split = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = -1, ()) =&gt; {
  splitReal(str, delim, take);
};
// let split: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;


---

split(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

split(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]


---

for (i in -3 to List.length(split(joinedStr, ())) + 2) {
  let (result, suffix) = try((split(joinedStr, ~take=i, ()), &quot;&quot;)) {
    | Invalid_argument(msg) =&gt; ([], &quot;Invalid argument: &quot; ++ msg)
  };
  
  let resultString = List.fold_left((acc, item) =&gt; acc == &quot;&quot; ? item : acc ++ &quot; &quot; ++ item, &quot;&quot;, result);
  print_endline(&quot;-- take: &quot; ++ string_of_int(i) ++ &quot;, result: &quot; ++ resultString ++ suffix);
};
/*
-- take: -3, result: Invalid argument: -3 &lt; -1 (wildcard)
-- take: -2, result: Invalid argument: -2 &lt; -1 (wildcard)
-- take: -1, result: a_b c_d e_f
-- take: 0, result: 
-- take: 1, result: a_b
-- take: 2, result: a_b c_d
-- take: 3, result: a_b c_d e_f
-- take: 4, result: Invalid argument: 4 &gt; 3 (length)
-- take: 5, result: Invalid argument: 5 &gt; 3 (length)
*/

---

split(&quot;&quot;, ());
// - : list(string) = [&quot;&quot;]


---

let splitSafe = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = str == &quot;&quot; ? 0 : -1, ()) =&gt; {
  split(str, ~delim=delim, ~take=take, ());
};
// let splitSafe: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

---

splitSafe(&quot;&quot;, ());
// - : list(string) = []


--- 

let splitSafer = (str: string, ~delim: option(char) = ?, ~take: option(int) = ?, ()) =&gt; {
  // This bit of logic ensures we&#x27;re always using sensible defaults.
  let newDelim = switch(delim) {
    | None =&gt; &#x27;,&#x27;
    | Some(value) =&gt; value
  };
  
  let newTake = switch(take) {
    | None =&gt; str == &quot;&quot; ? 0 : -1
    | Some(value) =&gt; value
  };

  // With these adjustments, we&#x27;re all set to make the split function even more user-friendly.
  split(str, ~delim=newDelim, ~take=newTake, ());
};
// let splitSafer: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;


--- 

splitSafer(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=?None, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

splitSafer(joinedStr, ~delim=?Some(&#x27;_&#x27;), ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split1.re

let joinedStr = &quot;a_b,c_d,e_f&quot;;
// let joinedStr: string = &quot;a_b,c_d,e_f&quot;;

String.split_on_char(&#x27;,&#x27;, joinedStr);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

String.split_on_char(&#x27;_&#x27;, joinedStr);
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split10.re

let splitSafer = (str: string, ~delim: option(char) = ?, ~take: option(int) = ?, ()) =&gt; {
  // This bit of logic ensures we&#x27;re always using sensible defaults.
  let newDelim = switch(delim) {
    | None =&gt; &#x27;,&#x27;
    | Some(value) =&gt; value
  };
  
  let newTake = switch(take) {
    | None =&gt; str == &quot;&quot; ? 0 : -1
    | Some(value) =&gt; value
  };

  // With these adjustments, we&#x27;re all set to make the split function even more user-friendly.
  split(str, ~delim=newDelim, ~take=newTake, ());
};
// let splitSafer: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

split11.re

splitSafer(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=?None, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

splitSafer(joinedStr, ~delim=?Some(&#x27;_&#x27;), ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split2.re

let splitReal = (str: string, delim: char, take: int) =&gt; {
  let values = String.split_on_char(delim, str);
  let len = List.length(values);
  
  // Keeping &#x27;take&#x27; within reasonable bounds was crucial. 
  if (take &gt; len) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &gt; &quot; ++ string_of_int(len) ++ &quot; (length)&quot;));
  };
  
  if (take &lt; -1) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &lt; -1 (wildcard)&quot;));
  };
  
  // Deciding on the exact number of pieces to take felt like balancing equations.
  let takeMod = if (take == -1) { // The wildcard case for all items.
    len &gt; 0 ? len - 1 : -1;
  } else { // Or just a specific count.
    len &gt; 0 &amp;&amp; take &gt; 0 ? (take - 1) mod len : -1;
  };
  
  // From there, it was about picking the right slices.
  let filteredValues = ref([]);
  for (i in 0 to takeMod) {
    filteredValues := List.append(filteredValues^, [List.nth(values, i)]);
  };
  filteredValues^;
}
// let splitReal: (string, char, int) =&gt; list(string) = &lt;fun&gt;;

split3.re

splitReal(joinedStr, &#x27;,&#x27;, -1);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

split4.re

let split = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = -1, ()) =&gt; {
  splitReal(str, delim, take);
};
// let split: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

split5.re

split(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

split(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split6.re

for (i in -3 to List.length(split(joinedStr, ())) + 2) {
  let (result, suffix) = try((split(joinedStr, ~take=i, ()), &quot;&quot;)) {
    | Invalid_argument(msg) =&gt; ([], &quot;Invalid argument: &quot; ++ msg)
  };
  
  let resultString = List.fold_left((acc, item) =&gt; acc == &quot;&quot; ? item : acc ++ &quot; &quot; ++ item, &quot;&quot;, result);
  print_endline(&quot;-- take: &quot; ++ string_of_int(i) ++ &quot;, result: &quot; ++ resultString ++ suffix);
};
/*
-- take: -3, result: Invalid argument: -3 &lt; -1 (wildcard)
-- take: -2, result: Invalid argument: -2 &lt; -1 (wildcard)
-- take: -1, result: a_b c_d e_f
-- take: 0, result: 
-- take: 1, result: a_b
-- take: 2, result: a_b c_d
-- take: 3, result: a_b c_d e_f
-- take: 4, result: Invalid argument: 4 &gt; 3 (length)
-- take: 5, result: Invalid argument: 5 &gt; 3 (length)
*/

split7.re

split(&quot;&quot;, ());
// - : list(string) = [&quot;&quot;]

split8.re

let splitSafe = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = str == &quot;&quot; ? 0 : -1, ()) =&gt; {
  split(str, ~delim=delim, ~take=take, ());
};
// let splitSafe: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

split9.re

splitSafe(&quot;&quot;, ());
// - : list(string) = []</code></pre><p>I couldn’t resist testing some edge cases, especially around the ‘take’ parameter. It’s like stress-testing your creation.</p><pre><code>Whole Split

split.re

let joinedStr = &quot;a_b,c_d,e_f&quot;;
// let joinedStr: string = &quot;a_b,c_d,e_f&quot;;

String.split_on_char(&#x27;,&#x27;, joinedStr);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

String.split_on_char(&#x27;_&#x27;, joinedStr);
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]


---

let splitReal = (str: string, delim: char, take: int) =&gt; {
  let values = String.split_on_char(delim, str);
  let len = List.length(values);
  
  // Keeping &#x27;take&#x27; within reasonable bounds was crucial. 
  if (take &gt; len) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &gt; &quot; ++ string_of_int(len) ++ &quot; (length)&quot;));
  };
  
  if (take &lt; -1) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &lt; -1 (wildcard)&quot;));
  };
  
  // Deciding on the exact number of pieces to take felt like balancing equations.
  let takeMod = if (take == -1) { // The wildcard case for all items.
    len &gt; 0 ? len - 1 : -1;
  } else { // Or just a specific count.
    len &gt; 0 &amp;&amp; take &gt; 0 ? (take - 1) mod len : -1;
  };
  
  // From there, it was about picking the right slices.
  let filteredValues = ref([]);
  for (i in 0 to takeMod) {
    filteredValues := List.append(filteredValues^, [List.nth(values, i)]);
  };
  filteredValues^;
}
// let splitReal: (string, char, int) =&gt; list(string) = &lt;fun&gt;;


---

splitReal(joinedStr, &#x27;,&#x27;, -1);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

---

let split = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = -1, ()) =&gt; {
  splitReal(str, delim, take);
};
// let split: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;


---

split(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

split(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]


---

for (i in -3 to List.length(split(joinedStr, ())) + 2) {
  let (result, suffix) = try((split(joinedStr, ~take=i, ()), &quot;&quot;)) {
    | Invalid_argument(msg) =&gt; ([], &quot;Invalid argument: &quot; ++ msg)
  };
  
  let resultString = List.fold_left((acc, item) =&gt; acc == &quot;&quot; ? item : acc ++ &quot; &quot; ++ item, &quot;&quot;, result);
  print_endline(&quot;-- take: &quot; ++ string_of_int(i) ++ &quot;, result: &quot; ++ resultString ++ suffix);
};
/*
-- take: -3, result: Invalid argument: -3 &lt; -1 (wildcard)
-- take: -2, result: Invalid argument: -2 &lt; -1 (wildcard)
-- take: -1, result: a_b c_d e_f
-- take: 0, result: 
-- take: 1, result: a_b
-- take: 2, result: a_b c_d
-- take: 3, result: a_b c_d e_f
-- take: 4, result: Invalid argument: 4 &gt; 3 (length)
-- take: 5, result: Invalid argument: 5 &gt; 3 (length)
*/

---

split(&quot;&quot;, ());
// - : list(string) = [&quot;&quot;]


---

let splitSafe = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = str == &quot;&quot; ? 0 : -1, ()) =&gt; {
  split(str, ~delim=delim, ~take=take, ());
};
// let splitSafe: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

---

splitSafe(&quot;&quot;, ());
// - : list(string) = []


--- 

let splitSafer = (str: string, ~delim: option(char) = ?, ~take: option(int) = ?, ()) =&gt; {
  // This bit of logic ensures we&#x27;re always using sensible defaults.
  let newDelim = switch(delim) {
    | None =&gt; &#x27;,&#x27;
    | Some(value) =&gt; value
  };
  
  let newTake = switch(take) {
    | None =&gt; str == &quot;&quot; ? 0 : -1
    | Some(value) =&gt; value
  };

  // With these adjustments, we&#x27;re all set to make the split function even more user-friendly.
  split(str, ~delim=newDelim, ~take=newTake, ());
};
// let splitSafer: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;


--- 

splitSafer(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=?None, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

splitSafer(joinedStr, ~delim=?Some(&#x27;_&#x27;), ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split1.re

let joinedStr = &quot;a_b,c_d,e_f&quot;;
// let joinedStr: string = &quot;a_b,c_d,e_f&quot;;

String.split_on_char(&#x27;,&#x27;, joinedStr);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

String.split_on_char(&#x27;_&#x27;, joinedStr);
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split10.re

let splitSafer = (str: string, ~delim: option(char) = ?, ~take: option(int) = ?, ()) =&gt; {
  // This bit of logic ensures we&#x27;re always using sensible defaults.
  let newDelim = switch(delim) {
    | None =&gt; &#x27;,&#x27;
    | Some(value) =&gt; value
  };
  
  let newTake = switch(take) {
    | None =&gt; str == &quot;&quot; ? 0 : -1
    | Some(value) =&gt; value
  };

  // With these adjustments, we&#x27;re all set to make the split function even more user-friendly.
  split(str, ~delim=newDelim, ~take=newTake, ());
};
// let splitSafer: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

split11.re

splitSafer(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=?None, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

splitSafer(joinedStr, ~delim=?Some(&#x27;_&#x27;), ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split2.re

let splitReal = (str: string, delim: char, take: int) =&gt; {
  let values = String.split_on_char(delim, str);
  let len = List.length(values);
  
  // Keeping &#x27;take&#x27; within reasonable bounds was crucial. 
  if (take &gt; len) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &gt; &quot; ++ string_of_int(len) ++ &quot; (length)&quot;));
  };
  
  if (take &lt; -1) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &lt; -1 (wildcard)&quot;));
  };
  
  // Deciding on the exact number of pieces to take felt like balancing equations.
  let takeMod = if (take == -1) { // The wildcard case for all items.
    len &gt; 0 ? len - 1 : -1;
  } else { // Or just a specific count.
    len &gt; 0 &amp;&amp; take &gt; 0 ? (take - 1) mod len : -1;
  };
  
  // From there, it was about picking the right slices.
  let filteredValues = ref([]);
  for (i in 0 to takeMod) {
    filteredValues := List.append(filteredValues^, [List.nth(values, i)]);
  };
  filteredValues^;
}
// let splitReal: (string, char, int) =&gt; list(string) = &lt;fun&gt;;

split3.re

splitReal(joinedStr, &#x27;,&#x27;, -1);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

split4.re

let split = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = -1, ()) =&gt; {
  splitReal(str, delim, take);
};
// let split: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

split5.re

split(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

split(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split6.re

for (i in -3 to List.length(split(joinedStr, ())) + 2) {
  let (result, suffix) = try((split(joinedStr, ~take=i, ()), &quot;&quot;)) {
    | Invalid_argument(msg) =&gt; ([], &quot;Invalid argument: &quot; ++ msg)
  };
  
  let resultString = List.fold_left((acc, item) =&gt; acc == &quot;&quot; ? item : acc ++ &quot; &quot; ++ item, &quot;&quot;, result);
  print_endline(&quot;-- take: &quot; ++ string_of_int(i) ++ &quot;, result: &quot; ++ resultString ++ suffix);
};
/*
-- take: -3, result: Invalid argument: -3 &lt; -1 (wildcard)
-- take: -2, result: Invalid argument: -2 &lt; -1 (wildcard)
-- take: -1, result: a_b c_d e_f
-- take: 0, result: 
-- take: 1, result: a_b
-- take: 2, result: a_b c_d
-- take: 3, result: a_b c_d e_f
-- take: 4, result: Invalid argument: 4 &gt; 3 (length)
-- take: 5, result: Invalid argument: 5 &gt; 3 (length)
*/

split7.re

split(&quot;&quot;, ());
// - : list(string) = [&quot;&quot;]

split8.re

let splitSafe = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = str == &quot;&quot; ? 0 : -1, ()) =&gt; {
  split(str, ~delim=delim, ~take=take, ());
};
// let splitSafe: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

split9.re

splitSafe(&quot;&quot;, ());
// - : list(string) = []</code></pre><p>Then, a curious bug popped up when testing on an empty string. Turns out, we need a bit more logic to handle that gracefully.</p><pre><code>Whole Split

split.re

let joinedStr = &quot;a_b,c_d,e_f&quot;;
// let joinedStr: string = &quot;a_b,c_d,e_f&quot;;

String.split_on_char(&#x27;,&#x27;, joinedStr);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

String.split_on_char(&#x27;_&#x27;, joinedStr);
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]


---

let splitReal = (str: string, delim: char, take: int) =&gt; {
  let values = String.split_on_char(delim, str);
  let len = List.length(values);
  
  // Keeping &#x27;take&#x27; within reasonable bounds was crucial. 
  if (take &gt; len) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &gt; &quot; ++ string_of_int(len) ++ &quot; (length)&quot;));
  };
  
  if (take &lt; -1) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &lt; -1 (wildcard)&quot;));
  };
  
  // Deciding on the exact number of pieces to take felt like balancing equations.
  let takeMod = if (take == -1) { // The wildcard case for all items.
    len &gt; 0 ? len - 1 : -1;
  } else { // Or just a specific count.
    len &gt; 0 &amp;&amp; take &gt; 0 ? (take - 1) mod len : -1;
  };
  
  // From there, it was about picking the right slices.
  let filteredValues = ref([]);
  for (i in 0 to takeMod) {
    filteredValues := List.append(filteredValues^, [List.nth(values, i)]);
  };
  filteredValues^;
}
// let splitReal: (string, char, int) =&gt; list(string) = &lt;fun&gt;;


---

splitReal(joinedStr, &#x27;,&#x27;, -1);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

---

let split = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = -1, ()) =&gt; {
  splitReal(str, delim, take);
};
// let split: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;


---

split(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

split(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]


---

for (i in -3 to List.length(split(joinedStr, ())) + 2) {
  let (result, suffix) = try((split(joinedStr, ~take=i, ()), &quot;&quot;)) {
    | Invalid_argument(msg) =&gt; ([], &quot;Invalid argument: &quot; ++ msg)
  };
  
  let resultString = List.fold_left((acc, item) =&gt; acc == &quot;&quot; ? item : acc ++ &quot; &quot; ++ item, &quot;&quot;, result);
  print_endline(&quot;-- take: &quot; ++ string_of_int(i) ++ &quot;, result: &quot; ++ resultString ++ suffix);
};
/*
-- take: -3, result: Invalid argument: -3 &lt; -1 (wildcard)
-- take: -2, result: Invalid argument: -2 &lt; -1 (wildcard)
-- take: -1, result: a_b c_d e_f
-- take: 0, result: 
-- take: 1, result: a_b
-- take: 2, result: a_b c_d
-- take: 3, result: a_b c_d e_f
-- take: 4, result: Invalid argument: 4 &gt; 3 (length)
-- take: 5, result: Invalid argument: 5 &gt; 3 (length)
*/

---

split(&quot;&quot;, ());
// - : list(string) = [&quot;&quot;]


---

let splitSafe = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = str == &quot;&quot; ? 0 : -1, ()) =&gt; {
  split(str, ~delim=delim, ~take=take, ());
};
// let splitSafe: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

---

splitSafe(&quot;&quot;, ());
// - : list(string) = []


--- 

let splitSafer = (str: string, ~delim: option(char) = ?, ~take: option(int) = ?, ()) =&gt; {
  // This bit of logic ensures we&#x27;re always using sensible defaults.
  let newDelim = switch(delim) {
    | None =&gt; &#x27;,&#x27;
    | Some(value) =&gt; value
  };
  
  let newTake = switch(take) {
    | None =&gt; str == &quot;&quot; ? 0 : -1
    | Some(value) =&gt; value
  };

  // With these adjustments, we&#x27;re all set to make the split function even more user-friendly.
  split(str, ~delim=newDelim, ~take=newTake, ());
};
// let splitSafer: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;


--- 

splitSafer(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=?None, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

splitSafer(joinedStr, ~delim=?Some(&#x27;_&#x27;), ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split1.re

let joinedStr = &quot;a_b,c_d,e_f&quot;;
// let joinedStr: string = &quot;a_b,c_d,e_f&quot;;

String.split_on_char(&#x27;,&#x27;, joinedStr);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

String.split_on_char(&#x27;_&#x27;, joinedStr);
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split10.re

let splitSafer = (str: string, ~delim: option(char) = ?, ~take: option(int) = ?, ()) =&gt; {
  // This bit of logic ensures we&#x27;re always using sensible defaults.
  let newDelim = switch(delim) {
    | None =&gt; &#x27;,&#x27;
    | Some(value) =&gt; value
  };
  
  let newTake = switch(take) {
    | None =&gt; str == &quot;&quot; ? 0 : -1
    | Some(value) =&gt; value
  };

  // With these adjustments, we&#x27;re all set to make the split function even more user-friendly.
  split(str, ~delim=newDelim, ~take=newTake, ());
};
// let splitSafer: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

split11.re

splitSafer(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=?None, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

splitSafer(joinedStr, ~delim=?Some(&#x27;_&#x27;), ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split2.re

let splitReal = (str: string, delim: char, take: int) =&gt; {
  let values = String.split_on_char(delim, str);
  let len = List.length(values);
  
  // Keeping &#x27;take&#x27; within reasonable bounds was crucial. 
  if (take &gt; len) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &gt; &quot; ++ string_of_int(len) ++ &quot; (length)&quot;));
  };
  
  if (take &lt; -1) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &lt; -1 (wildcard)&quot;));
  };
  
  // Deciding on the exact number of pieces to take felt like balancing equations.
  let takeMod = if (take == -1) { // The wildcard case for all items.
    len &gt; 0 ? len - 1 : -1;
  } else { // Or just a specific count.
    len &gt; 0 &amp;&amp; take &gt; 0 ? (take - 1) mod len : -1;
  };
  
  // From there, it was about picking the right slices.
  let filteredValues = ref([]);
  for (i in 0 to takeMod) {
    filteredValues := List.append(filteredValues^, [List.nth(values, i)]);
  };
  filteredValues^;
}
// let splitReal: (string, char, int) =&gt; list(string) = &lt;fun&gt;;

split3.re

splitReal(joinedStr, &#x27;,&#x27;, -1);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

split4.re

let split = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = -1, ()) =&gt; {
  splitReal(str, delim, take);
};
// let split: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

split5.re

split(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

split(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split6.re

for (i in -3 to List.length(split(joinedStr, ())) + 2) {
  let (result, suffix) = try((split(joinedStr, ~take=i, ()), &quot;&quot;)) {
    | Invalid_argument(msg) =&gt; ([], &quot;Invalid argument: &quot; ++ msg)
  };
  
  let resultString = List.fold_left((acc, item) =&gt; acc == &quot;&quot; ? item : acc ++ &quot; &quot; ++ item, &quot;&quot;, result);
  print_endline(&quot;-- take: &quot; ++ string_of_int(i) ++ &quot;, result: &quot; ++ resultString ++ suffix);
};
/*
-- take: -3, result: Invalid argument: -3 &lt; -1 (wildcard)
-- take: -2, result: Invalid argument: -2 &lt; -1 (wildcard)
-- take: -1, result: a_b c_d e_f
-- take: 0, result: 
-- take: 1, result: a_b
-- take: 2, result: a_b c_d
-- take: 3, result: a_b c_d e_f
-- take: 4, result: Invalid argument: 4 &gt; 3 (length)
-- take: 5, result: Invalid argument: 5 &gt; 3 (length)
*/

split7.re

split(&quot;&quot;, ());
// - : list(string) = [&quot;&quot;]

split8.re

let splitSafe = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = str == &quot;&quot; ? 0 : -1, ()) =&gt; {
  split(str, ~delim=delim, ~take=take, ());
};
// let splitSafe: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

split9.re

splitSafe(&quot;&quot;, ());
// - : list(string) = []</code></pre><p>Adjusting the ‘take’ value based on whether the string is empty was the fix. It felt like plugging a leak in a dam.</p><pre><code>Whole Split

split.re

let joinedStr = &quot;a_b,c_d,e_f&quot;;
// let joinedStr: string = &quot;a_b,c_d,e_f&quot;;

String.split_on_char(&#x27;,&#x27;, joinedStr);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

String.split_on_char(&#x27;_&#x27;, joinedStr);
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]


---

let splitReal = (str: string, delim: char, take: int) =&gt; {
  let values = String.split_on_char(delim, str);
  let len = List.length(values);
  
  // Keeping &#x27;take&#x27; within reasonable bounds was crucial. 
  if (take &gt; len) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &gt; &quot; ++ string_of_int(len) ++ &quot; (length)&quot;));
  };
  
  if (take &lt; -1) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &lt; -1 (wildcard)&quot;));
  };
  
  // Deciding on the exact number of pieces to take felt like balancing equations.
  let takeMod = if (take == -1) { // The wildcard case for all items.
    len &gt; 0 ? len - 1 : -1;
  } else { // Or just a specific count.
    len &gt; 0 &amp;&amp; take &gt; 0 ? (take - 1) mod len : -1;
  };
  
  // From there, it was about picking the right slices.
  let filteredValues = ref([]);
  for (i in 0 to takeMod) {
    filteredValues := List.append(filteredValues^, [List.nth(values, i)]);
  };
  filteredValues^;
}
// let splitReal: (string, char, int) =&gt; list(string) = &lt;fun&gt;;


---

splitReal(joinedStr, &#x27;,&#x27;, -1);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

---

let split = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = -1, ()) =&gt; {
  splitReal(str, delim, take);
};
// let split: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;


---

split(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

split(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]


---

for (i in -3 to List.length(split(joinedStr, ())) + 2) {
  let (result, suffix) = try((split(joinedStr, ~take=i, ()), &quot;&quot;)) {
    | Invalid_argument(msg) =&gt; ([], &quot;Invalid argument: &quot; ++ msg)
  };
  
  let resultString = List.fold_left((acc, item) =&gt; acc == &quot;&quot; ? item : acc ++ &quot; &quot; ++ item, &quot;&quot;, result);
  print_endline(&quot;-- take: &quot; ++ string_of_int(i) ++ &quot;, result: &quot; ++ resultString ++ suffix);
};
/*
-- take: -3, result: Invalid argument: -3 &lt; -1 (wildcard)
-- take: -2, result: Invalid argument: -2 &lt; -1 (wildcard)
-- take: -1, result: a_b c_d e_f
-- take: 0, result: 
-- take: 1, result: a_b
-- take: 2, result: a_b c_d
-- take: 3, result: a_b c_d e_f
-- take: 4, result: Invalid argument: 4 &gt; 3 (length)
-- take: 5, result: Invalid argument: 5 &gt; 3 (length)
*/

---

split(&quot;&quot;, ());
// - : list(string) = [&quot;&quot;]


---

let splitSafe = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = str == &quot;&quot; ? 0 : -1, ()) =&gt; {
  split(str, ~delim=delim, ~take=take, ());
};
// let splitSafe: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

---

splitSafe(&quot;&quot;, ());
// - : list(string) = []


--- 

let splitSafer = (str: string, ~delim: option(char) = ?, ~take: option(int) = ?, ()) =&gt; {
  // This bit of logic ensures we&#x27;re always using sensible defaults.
  let newDelim = switch(delim) {
    | None =&gt; &#x27;,&#x27;
    | Some(value) =&gt; value
  };
  
  let newTake = switch(take) {
    | None =&gt; str == &quot;&quot; ? 0 : -1
    | Some(value) =&gt; value
  };

  // With these adjustments, we&#x27;re all set to make the split function even more user-friendly.
  split(str, ~delim=newDelim, ~take=newTake, ());
};
// let splitSafer: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;


--- 

splitSafer(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=?None, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

splitSafer(joinedStr, ~delim=?Some(&#x27;_&#x27;), ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split1.re

let joinedStr = &quot;a_b,c_d,e_f&quot;;
// let joinedStr: string = &quot;a_b,c_d,e_f&quot;;

String.split_on_char(&#x27;,&#x27;, joinedStr);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

String.split_on_char(&#x27;_&#x27;, joinedStr);
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split10.re

let splitSafer = (str: string, ~delim: option(char) = ?, ~take: option(int) = ?, ()) =&gt; {
  // This bit of logic ensures we&#x27;re always using sensible defaults.
  let newDelim = switch(delim) {
    | None =&gt; &#x27;,&#x27;
    | Some(value) =&gt; value
  };
  
  let newTake = switch(take) {
    | None =&gt; str == &quot;&quot; ? 0 : -1
    | Some(value) =&gt; value
  };

  // With these adjustments, we&#x27;re all set to make the split function even more user-friendly.
  split(str, ~delim=newDelim, ~take=newTake, ());
};
// let splitSafer: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

split11.re

splitSafer(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=?None, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

splitSafer(joinedStr, ~delim=?Some(&#x27;_&#x27;), ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split2.re

let splitReal = (str: string, delim: char, take: int) =&gt; {
  let values = String.split_on_char(delim, str);
  let len = List.length(values);
  
  // Keeping &#x27;take&#x27; within reasonable bounds was crucial. 
  if (take &gt; len) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &gt; &quot; ++ string_of_int(len) ++ &quot; (length)&quot;));
  };
  
  if (take &lt; -1) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &lt; -1 (wildcard)&quot;));
  };
  
  // Deciding on the exact number of pieces to take felt like balancing equations.
  let takeMod = if (take == -1) { // The wildcard case for all items.
    len &gt; 0 ? len - 1 : -1;
  } else { // Or just a specific count.
    len &gt; 0 &amp;&amp; take &gt; 0 ? (take - 1) mod len : -1;
  };
  
  // From there, it was about picking the right slices.
  let filteredValues = ref([]);
  for (i in 0 to takeMod) {
    filteredValues := List.append(filteredValues^, [List.nth(values, i)]);
  };
  filteredValues^;
}
// let splitReal: (string, char, int) =&gt; list(string) = &lt;fun&gt;;

split3.re

splitReal(joinedStr, &#x27;,&#x27;, -1);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

split4.re

let split = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = -1, ()) =&gt; {
  splitReal(str, delim, take);
};
// let split: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

split5.re

split(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

split(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split6.re

for (i in -3 to List.length(split(joinedStr, ())) + 2) {
  let (result, suffix) = try((split(joinedStr, ~take=i, ()), &quot;&quot;)) {
    | Invalid_argument(msg) =&gt; ([], &quot;Invalid argument: &quot; ++ msg)
  };
  
  let resultString = List.fold_left((acc, item) =&gt; acc == &quot;&quot; ? item : acc ++ &quot; &quot; ++ item, &quot;&quot;, result);
  print_endline(&quot;-- take: &quot; ++ string_of_int(i) ++ &quot;, result: &quot; ++ resultString ++ suffix);
};
/*
-- take: -3, result: Invalid argument: -3 &lt; -1 (wildcard)
-- take: -2, result: Invalid argument: -2 &lt; -1 (wildcard)
-- take: -1, result: a_b c_d e_f
-- take: 0, result: 
-- take: 1, result: a_b
-- take: 2, result: a_b c_d
-- take: 3, result: a_b c_d e_f
-- take: 4, result: Invalid argument: 4 &gt; 3 (length)
-- take: 5, result: Invalid argument: 5 &gt; 3 (length)
*/

split7.re

split(&quot;&quot;, ());
// - : list(string) = [&quot;&quot;]

split8.re

let splitSafe = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = str == &quot;&quot; ? 0 : -1, ()) =&gt; {
  split(str, ~delim=delim, ~take=take, ());
};
// let splitSafe: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

split9.re

splitSafe(&quot;&quot;, ());
// - : list(string) = []</code></pre><p>And voilà, the bug was squashed. It’s little victories like this that make coding fun.</p><pre><code>Whole Split

split.re

let joinedStr = &quot;a_b,c_d,e_f&quot;;
// let joinedStr: string = &quot;a_b,c_d,e_f&quot;;

String.split_on_char(&#x27;,&#x27;, joinedStr);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

String.split_on_char(&#x27;_&#x27;, joinedStr);
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]


---

let splitReal = (str: string, delim: char, take: int) =&gt; {
  let values = String.split_on_char(delim, str);
  let len = List.length(values);
  
  // Keeping &#x27;take&#x27; within reasonable bounds was crucial. 
  if (take &gt; len) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &gt; &quot; ++ string_of_int(len) ++ &quot; (length)&quot;));
  };
  
  if (take &lt; -1) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &lt; -1 (wildcard)&quot;));
  };
  
  // Deciding on the exact number of pieces to take felt like balancing equations.
  let takeMod = if (take == -1) { // The wildcard case for all items.
    len &gt; 0 ? len - 1 : -1;
  } else { // Or just a specific count.
    len &gt; 0 &amp;&amp; take &gt; 0 ? (take - 1) mod len : -1;
  };
  
  // From there, it was about picking the right slices.
  let filteredValues = ref([]);
  for (i in 0 to takeMod) {
    filteredValues := List.append(filteredValues^, [List.nth(values, i)]);
  };
  filteredValues^;
}
// let splitReal: (string, char, int) =&gt; list(string) = &lt;fun&gt;;


---

splitReal(joinedStr, &#x27;,&#x27;, -1);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

---

let split = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = -1, ()) =&gt; {
  splitReal(str, delim, take);
};
// let split: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;


---

split(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

split(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]


---

for (i in -3 to List.length(split(joinedStr, ())) + 2) {
  let (result, suffix) = try((split(joinedStr, ~take=i, ()), &quot;&quot;)) {
    | Invalid_argument(msg) =&gt; ([], &quot;Invalid argument: &quot; ++ msg)
  };
  
  let resultString = List.fold_left((acc, item) =&gt; acc == &quot;&quot; ? item : acc ++ &quot; &quot; ++ item, &quot;&quot;, result);
  print_endline(&quot;-- take: &quot; ++ string_of_int(i) ++ &quot;, result: &quot; ++ resultString ++ suffix);
};
/*
-- take: -3, result: Invalid argument: -3 &lt; -1 (wildcard)
-- take: -2, result: Invalid argument: -2 &lt; -1 (wildcard)
-- take: -1, result: a_b c_d e_f
-- take: 0, result: 
-- take: 1, result: a_b
-- take: 2, result: a_b c_d
-- take: 3, result: a_b c_d e_f
-- take: 4, result: Invalid argument: 4 &gt; 3 (length)
-- take: 5, result: Invalid argument: 5 &gt; 3 (length)
*/

---

split(&quot;&quot;, ());
// - : list(string) = [&quot;&quot;]


---

let splitSafe = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = str == &quot;&quot; ? 0 : -1, ()) =&gt; {
  split(str, ~delim=delim, ~take=take, ());
};
// let splitSafe: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

---

splitSafe(&quot;&quot;, ());
// - : list(string) = []


--- 

let splitSafer = (str: string, ~delim: option(char) = ?, ~take: option(int) = ?, ()) =&gt; {
  // This bit of logic ensures we&#x27;re always using sensible defaults.
  let newDelim = switch(delim) {
    | None =&gt; &#x27;,&#x27;
    | Some(value) =&gt; value
  };
  
  let newTake = switch(take) {
    | None =&gt; str == &quot;&quot; ? 0 : -1
    | Some(value) =&gt; value
  };

  // With these adjustments, we&#x27;re all set to make the split function even more user-friendly.
  split(str, ~delim=newDelim, ~take=newTake, ());
};
// let splitSafer: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;


--- 

splitSafer(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=?None, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

splitSafer(joinedStr, ~delim=?Some(&#x27;_&#x27;), ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split1.re

let joinedStr = &quot;a_b,c_d,e_f&quot;;
// let joinedStr: string = &quot;a_b,c_d,e_f&quot;;

String.split_on_char(&#x27;,&#x27;, joinedStr);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

String.split_on_char(&#x27;_&#x27;, joinedStr);
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split10.re

let splitSafer = (str: string, ~delim: option(char) = ?, ~take: option(int) = ?, ()) =&gt; {
  // This bit of logic ensures we&#x27;re always using sensible defaults.
  let newDelim = switch(delim) {
    | None =&gt; &#x27;,&#x27;
    | Some(value) =&gt; value
  };
  
  let newTake = switch(take) {
    | None =&gt; str == &quot;&quot; ? 0 : -1
    | Some(value) =&gt; value
  };

  // With these adjustments, we&#x27;re all set to make the split function even more user-friendly.
  split(str, ~delim=newDelim, ~take=newTake, ());
};
// let splitSafer: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

split11.re

splitSafer(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=?None, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

splitSafer(joinedStr, ~delim=?Some(&#x27;_&#x27;), ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split2.re

let splitReal = (str: string, delim: char, take: int) =&gt; {
  let values = String.split_on_char(delim, str);
  let len = List.length(values);
  
  // Keeping &#x27;take&#x27; within reasonable bounds was crucial. 
  if (take &gt; len) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &gt; &quot; ++ string_of_int(len) ++ &quot; (length)&quot;));
  };
  
  if (take &lt; -1) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &lt; -1 (wildcard)&quot;));
  };
  
  // Deciding on the exact number of pieces to take felt like balancing equations.
  let takeMod = if (take == -1) { // The wildcard case for all items.
    len &gt; 0 ? len - 1 : -1;
  } else { // Or just a specific count.
    len &gt; 0 &amp;&amp; take &gt; 0 ? (take - 1) mod len : -1;
  };
  
  // From there, it was about picking the right slices.
  let filteredValues = ref([]);
  for (i in 0 to takeMod) {
    filteredValues := List.append(filteredValues^, [List.nth(values, i)]);
  };
  filteredValues^;
}
// let splitReal: (string, char, int) =&gt; list(string) = &lt;fun&gt;;

split3.re

splitReal(joinedStr, &#x27;,&#x27;, -1);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

split4.re

let split = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = -1, ()) =&gt; {
  splitReal(str, delim, take);
};
// let split: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

split5.re

split(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

split(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split6.re

for (i in -3 to List.length(split(joinedStr, ())) + 2) {
  let (result, suffix) = try((split(joinedStr, ~take=i, ()), &quot;&quot;)) {
    | Invalid_argument(msg) =&gt; ([], &quot;Invalid argument: &quot; ++ msg)
  };
  
  let resultString = List.fold_left((acc, item) =&gt; acc == &quot;&quot; ? item : acc ++ &quot; &quot; ++ item, &quot;&quot;, result);
  print_endline(&quot;-- take: &quot; ++ string_of_int(i) ++ &quot;, result: &quot; ++ resultString ++ suffix);
};
/*
-- take: -3, result: Invalid argument: -3 &lt; -1 (wildcard)
-- take: -2, result: Invalid argument: -2 &lt; -1 (wildcard)
-- take: -1, result: a_b c_d e_f
-- take: 0, result: 
-- take: 1, result: a_b
-- take: 2, result: a_b c_d
-- take: 3, result: a_b c_d e_f
-- take: 4, result: Invalid argument: 4 &gt; 3 (length)
-- take: 5, result: Invalid argument: 5 &gt; 3 (length)
*/

split7.re

split(&quot;&quot;, ());
// - : list(string) = [&quot;&quot;]

split8.re

let splitSafe = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = str == &quot;&quot; ? 0 : -1, ()) =&gt; {
  split(str, ~delim=delim, ~take=take, ());
};
// let splitSafe: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

split9.re

splitSafe(&quot;&quot;, ());
// - : list(string) = []</code></pre><p>Finally, to make the function even more robust, I tackled a scope-related issue, making sure defaults are handled cleanly.</p><pre><code>Whole Split

split.re

let joinedStr = &quot;a_b,c_d,e_f&quot;;
// let joinedStr: string = &quot;a_b,c_d,e_f&quot;;

String.split_on_char(&#x27;,&#x27;, joinedStr);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

String.split_on_char(&#x27;_&#x27;, joinedStr);
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]


---

let splitReal = (str: string, delim: char, take: int) =&gt; {
  let values = String.split_on_char(delim, str);
  let len = List.length(values);
  
  // Keeping &#x27;take&#x27; within reasonable bounds was crucial. 
  if (take &gt; len) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &gt; &quot; ++ string_of_int(len) ++ &quot; (length)&quot;));
  };
  
  if (take &lt; -1) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &lt; -1 (wildcard)&quot;));
  };
  
  // Deciding on the exact number of pieces to take felt like balancing equations.
  let takeMod = if (take == -1) { // The wildcard case for all items.
    len &gt; 0 ? len - 1 : -1;
  } else { // Or just a specific count.
    len &gt; 0 &amp;&amp; take &gt; 0 ? (take - 1) mod len : -1;
  };
  
  // From there, it was about picking the right slices.
  let filteredValues = ref([]);
  for (i in 0 to takeMod) {
    filteredValues := List.append(filteredValues^, [List.nth(values, i)]);
  };
  filteredValues^;
}
// let splitReal: (string, char, int) =&gt; list(string) = &lt;fun&gt;;


---

splitReal(joinedStr, &#x27;,&#x27;, -1);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

---

let split = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = -1, ()) =&gt; {
  splitReal(str, delim, take);
};
// let split: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;


---

split(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

split(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]


---

for (i in -3 to List.length(split(joinedStr, ())) + 2) {
  let (result, suffix) = try((split(joinedStr, ~take=i, ()), &quot;&quot;)) {
    | Invalid_argument(msg) =&gt; ([], &quot;Invalid argument: &quot; ++ msg)
  };
  
  let resultString = List.fold_left((acc, item) =&gt; acc == &quot;&quot; ? item : acc ++ &quot; &quot; ++ item, &quot;&quot;, result);
  print_endline(&quot;-- take: &quot; ++ string_of_int(i) ++ &quot;, result: &quot; ++ resultString ++ suffix);
};
/*
-- take: -3, result: Invalid argument: -3 &lt; -1 (wildcard)
-- take: -2, result: Invalid argument: -2 &lt; -1 (wildcard)
-- take: -1, result: a_b c_d e_f
-- take: 0, result: 
-- take: 1, result: a_b
-- take: 2, result: a_b c_d
-- take: 3, result: a_b c_d e_f
-- take: 4, result: Invalid argument: 4 &gt; 3 (length)
-- take: 5, result: Invalid argument: 5 &gt; 3 (length)
*/

---

split(&quot;&quot;, ());
// - : list(string) = [&quot;&quot;]


---

let splitSafe = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = str == &quot;&quot; ? 0 : -1, ()) =&gt; {
  split(str, ~delim=delim, ~take=take, ());
};
// let splitSafe: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

---

splitSafe(&quot;&quot;, ());
// - : list(string) = []


--- 

let splitSafer = (str: string, ~delim: option(char) = ?, ~take: option(int) = ?, ()) =&gt; {
  // This bit of logic ensures we&#x27;re always using sensible defaults.
  let newDelim = switch(delim) {
    | None =&gt; &#x27;,&#x27;
    | Some(value) =&gt; value
  };
  
  let newTake = switch(take) {
    | None =&gt; str == &quot;&quot; ? 0 : -1
    | Some(value) =&gt; value
  };

  // With these adjustments, we&#x27;re all set to make the split function even more user-friendly.
  split(str, ~delim=newDelim, ~take=newTake, ());
};
// let splitSafer: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;


--- 

splitSafer(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=?None, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

splitSafer(joinedStr, ~delim=?Some(&#x27;_&#x27;), ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split1.re

let joinedStr = &quot;a_b,c_d,e_f&quot;;
// let joinedStr: string = &quot;a_b,c_d,e_f&quot;;

String.split_on_char(&#x27;,&#x27;, joinedStr);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

String.split_on_char(&#x27;_&#x27;, joinedStr);
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split10.re

let splitSafer = (str: string, ~delim: option(char) = ?, ~take: option(int) = ?, ()) =&gt; {
  // This bit of logic ensures we&#x27;re always using sensible defaults.
  let newDelim = switch(delim) {
    | None =&gt; &#x27;,&#x27;
    | Some(value) =&gt; value
  };
  
  let newTake = switch(take) {
    | None =&gt; str == &quot;&quot; ? 0 : -1
    | Some(value) =&gt; value
  };

  // With these adjustments, we&#x27;re all set to make the split function even more user-friendly.
  split(str, ~delim=newDelim, ~take=newTake, ());
};
// let splitSafer: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

split11.re

splitSafer(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=?None, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

splitSafer(joinedStr, ~delim=?Some(&#x27;_&#x27;), ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split2.re

let splitReal = (str: string, delim: char, take: int) =&gt; {
  let values = String.split_on_char(delim, str);
  let len = List.length(values);
  
  // Keeping &#x27;take&#x27; within reasonable bounds was crucial. 
  if (take &gt; len) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &gt; &quot; ++ string_of_int(len) ++ &quot; (length)&quot;));
  };
  
  if (take &lt; -1) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &lt; -1 (wildcard)&quot;));
  };
  
  // Deciding on the exact number of pieces to take felt like balancing equations.
  let takeMod = if (take == -1) { // The wildcard case for all items.
    len &gt; 0 ? len - 1 : -1;
  } else { // Or just a specific count.
    len &gt; 0 &amp;&amp; take &gt; 0 ? (take - 1) mod len : -1;
  };
  
  // From there, it was about picking the right slices.
  let filteredValues = ref([]);
  for (i in 0 to takeMod) {
    filteredValues := List.append(filteredValues^, [List.nth(values, i)]);
  };
  filteredValues^;
}
// let splitReal: (string, char, int) =&gt; list(string) = &lt;fun&gt;;

split3.re

splitReal(joinedStr, &#x27;,&#x27;, -1);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

split4.re

let split = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = -1, ()) =&gt; {
  splitReal(str, delim, take);
};
// let split: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

split5.re

split(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

split(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split6.re

for (i in -3 to List.length(split(joinedStr, ())) + 2) {
  let (result, suffix) = try((split(joinedStr, ~take=i, ()), &quot;&quot;)) {
    | Invalid_argument(msg) =&gt; ([], &quot;Invalid argument: &quot; ++ msg)
  };
  
  let resultString = List.fold_left((acc, item) =&gt; acc == &quot;&quot; ? item : acc ++ &quot; &quot; ++ item, &quot;&quot;, result);
  print_endline(&quot;-- take: &quot; ++ string_of_int(i) ++ &quot;, result: &quot; ++ resultString ++ suffix);
};
/*
-- take: -3, result: Invalid argument: -3 &lt; -1 (wildcard)
-- take: -2, result: Invalid argument: -2 &lt; -1 (wildcard)
-- take: -1, result: a_b c_d e_f
-- take: 0, result: 
-- take: 1, result: a_b
-- take: 2, result: a_b c_d
-- take: 3, result: a_b c_d e_f
-- take: 4, result: Invalid argument: 4 &gt; 3 (length)
-- take: 5, result: Invalid argument: 5 &gt; 3 (length)
*/

split7.re

split(&quot;&quot;, ());
// - : list(string) = [&quot;&quot;]

split8.re

let splitSafe = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = str == &quot;&quot; ? 0 : -1, ()) =&gt; {
  split(str, ~delim=delim, ~take=take, ());
};
// let splitSafe: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

split9.re

splitSafe(&quot;&quot;, ());
// - : list(string) = []</code></pre><p>With these adjustments, we’re all set to make the split function even more user-friendly.</p><pre><code>Whole Split

split.re

let joinedStr = &quot;a_b,c_d,e_f&quot;;
// let joinedStr: string = &quot;a_b,c_d,e_f&quot;;

String.split_on_char(&#x27;,&#x27;, joinedStr);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

String.split_on_char(&#x27;_&#x27;, joinedStr);
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]


---

let splitReal = (str: string, delim: char, take: int) =&gt; {
  let values = String.split_on_char(delim, str);
  let len = List.length(values);
  
  // Keeping &#x27;take&#x27; within reasonable bounds was crucial. 
  if (take &gt; len) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &gt; &quot; ++ string_of_int(len) ++ &quot; (length)&quot;));
  };
  
  if (take &lt; -1) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &lt; -1 (wildcard)&quot;));
  };
  
  // Deciding on the exact number of pieces to take felt like balancing equations.
  let takeMod = if (take == -1) { // The wildcard case for all items.
    len &gt; 0 ? len - 1 : -1;
  } else { // Or just a specific count.
    len &gt; 0 &amp;&amp; take &gt; 0 ? (take - 1) mod len : -1;
  };
  
  // From there, it was about picking the right slices.
  let filteredValues = ref([]);
  for (i in 0 to takeMod) {
    filteredValues := List.append(filteredValues^, [List.nth(values, i)]);
  };
  filteredValues^;
}
// let splitReal: (string, char, int) =&gt; list(string) = &lt;fun&gt;;


---

splitReal(joinedStr, &#x27;,&#x27;, -1);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

---

let split = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = -1, ()) =&gt; {
  splitReal(str, delim, take);
};
// let split: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;


---

split(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

split(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]


---

for (i in -3 to List.length(split(joinedStr, ())) + 2) {
  let (result, suffix) = try((split(joinedStr, ~take=i, ()), &quot;&quot;)) {
    | Invalid_argument(msg) =&gt; ([], &quot;Invalid argument: &quot; ++ msg)
  };
  
  let resultString = List.fold_left((acc, item) =&gt; acc == &quot;&quot; ? item : acc ++ &quot; &quot; ++ item, &quot;&quot;, result);
  print_endline(&quot;-- take: &quot; ++ string_of_int(i) ++ &quot;, result: &quot; ++ resultString ++ suffix);
};
/*
-- take: -3, result: Invalid argument: -3 &lt; -1 (wildcard)
-- take: -2, result: Invalid argument: -2 &lt; -1 (wildcard)
-- take: -1, result: a_b c_d e_f
-- take: 0, result: 
-- take: 1, result: a_b
-- take: 2, result: a_b c_d
-- take: 3, result: a_b c_d e_f
-- take: 4, result: Invalid argument: 4 &gt; 3 (length)
-- take: 5, result: Invalid argument: 5 &gt; 3 (length)
*/

---

split(&quot;&quot;, ());
// - : list(string) = [&quot;&quot;]


---

let splitSafe = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = str == &quot;&quot; ? 0 : -1, ()) =&gt; {
  split(str, ~delim=delim, ~take=take, ());
};
// let splitSafe: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

---

splitSafe(&quot;&quot;, ());
// - : list(string) = []


--- 

let splitSafer = (str: string, ~delim: option(char) = ?, ~take: option(int) = ?, ()) =&gt; {
  // This bit of logic ensures we&#x27;re always using sensible defaults.
  let newDelim = switch(delim) {
    | None =&gt; &#x27;,&#x27;
    | Some(value) =&gt; value
  };
  
  let newTake = switch(take) {
    | None =&gt; str == &quot;&quot; ? 0 : -1
    | Some(value) =&gt; value
  };

  // With these adjustments, we&#x27;re all set to make the split function even more user-friendly.
  split(str, ~delim=newDelim, ~take=newTake, ());
};
// let splitSafer: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;


--- 

splitSafer(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=?None, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

splitSafer(joinedStr, ~delim=?Some(&#x27;_&#x27;), ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split1.re

let joinedStr = &quot;a_b,c_d,e_f&quot;;
// let joinedStr: string = &quot;a_b,c_d,e_f&quot;;

String.split_on_char(&#x27;,&#x27;, joinedStr);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

String.split_on_char(&#x27;_&#x27;, joinedStr);
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split10.re

let splitSafer = (str: string, ~delim: option(char) = ?, ~take: option(int) = ?, ()) =&gt; {
  // This bit of logic ensures we&#x27;re always using sensible defaults.
  let newDelim = switch(delim) {
    | None =&gt; &#x27;,&#x27;
    | Some(value) =&gt; value
  };
  
  let newTake = switch(take) {
    | None =&gt; str == &quot;&quot; ? 0 : -1
    | Some(value) =&gt; value
  };

  // With these adjustments, we&#x27;re all set to make the split function even more user-friendly.
  split(str, ~delim=newDelim, ~take=newTake, ());
};
// let splitSafer: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

split11.re

splitSafer(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=?None, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

splitSafer(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

splitSafer(joinedStr, ~delim=?Some(&#x27;_&#x27;), ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split2.re

let splitReal = (str: string, delim: char, take: int) =&gt; {
  let values = String.split_on_char(delim, str);
  let len = List.length(values);
  
  // Keeping &#x27;take&#x27; within reasonable bounds was crucial. 
  if (take &gt; len) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &gt; &quot; ++ string_of_int(len) ++ &quot; (length)&quot;));
  };
  
  if (take &lt; -1) {
    raise(Invalid_argument(string_of_int(take) ++ &quot; &lt; -1 (wildcard)&quot;));
  };
  
  // Deciding on the exact number of pieces to take felt like balancing equations.
  let takeMod = if (take == -1) { // The wildcard case for all items.
    len &gt; 0 ? len - 1 : -1;
  } else { // Or just a specific count.
    len &gt; 0 &amp;&amp; take &gt; 0 ? (take - 1) mod len : -1;
  };
  
  // From there, it was about picking the right slices.
  let filteredValues = ref([]);
  for (i in 0 to takeMod) {
    filteredValues := List.append(filteredValues^, [List.nth(values, i)]);
  };
  filteredValues^;
}
// let splitReal: (string, char, int) =&gt; list(string) = &lt;fun&gt;;

split3.re

splitReal(joinedStr, &#x27;,&#x27;, -1);
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

split4.re

let split = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = -1, ()) =&gt; {
  splitReal(str, delim, take);
};
// let split: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

split5.re

split(joinedStr, ());
// - : list(string) = [&quot;a_b&quot;, &quot;c_d&quot;, &quot;e_f&quot;]

split(joinedStr, ~delim=&#x27;_&#x27;, ());
// - : list(string) = [&quot;a&quot;, &quot;b,c&quot;, &quot;d,e&quot;, &quot;f&quot;]

split6.re

for (i in -3 to List.length(split(joinedStr, ())) + 2) {
  let (result, suffix) = try((split(joinedStr, ~take=i, ()), &quot;&quot;)) {
    | Invalid_argument(msg) =&gt; ([], &quot;Invalid argument: &quot; ++ msg)
  };
  
  let resultString = List.fold_left((acc, item) =&gt; acc == &quot;&quot; ? item : acc ++ &quot; &quot; ++ item, &quot;&quot;, result);
  print_endline(&quot;-- take: &quot; ++ string_of_int(i) ++ &quot;, result: &quot; ++ resultString ++ suffix);
};
/*
-- take: -3, result: Invalid argument: -3 &lt; -1 (wildcard)
-- take: -2, result: Invalid argument: -2 &lt; -1 (wildcard)
-- take: -1, result: a_b c_d e_f
-- take: 0, result: 
-- take: 1, result: a_b
-- take: 2, result: a_b c_d
-- take: 3, result: a_b c_d e_f
-- take: 4, result: Invalid argument: 4 &gt; 3 (length)
-- take: 5, result: Invalid argument: 5 &gt; 3 (length)
*/

split7.re

split(&quot;&quot;, ());
// - : list(string) = [&quot;&quot;]

split8.re

let splitSafe = (str: string, ~delim: char = &#x27;,&#x27;, ~take: int = str == &quot;&quot; ? 0 : -1, ()) =&gt; {
  split(str, ~delim=delim, ~take=take, ());
};
// let splitSafe: (string, ~delim: char=?, ~take: int=?, unit) =&gt; list(string) =
  &lt;fun&gt;;

split9.re

splitSafe(&quot;&quot;, ());
// - : list(string) = []</code></pre><p>What’s cool about ReasonML is how it lets us handle these optional parameters with grace. It’s like giving the function a mind of its own, smartly adjusting to what it’s given.</p><p>Now, making function calls is as easy as pie. Whether you specify parameters or not, it just works.</p><p>Reflecting on this journey, what started as a straightforward task evolved into a deep dive into the nuances of function design in ReasonML. Along the way, I not only tackled unexpected challenges but also discovered the joy of crafting code that’s both elegant and robust.</p><p>Every bug squashed and every edge case covered brought a sense of accomplishment. It’s these moments that remind me why I love coding: the continuous learning, the problem-solving thrill, and the satisfaction of building something that works well.</p><p>So there you have it, a journey through the creation of a safe string splitting function in ReasonML. It’s been a rewarding adventure, full of learning and fine-tuning. And who knows? The next challenge is just around the corner, ready to push our coding skills even further.</p><p>For quick navigation, here are the other articles in the same series:</p><p><a href="https://yamaceay.medium.com/learn-with-me-reasonml-part-2-6f704e0ded0b">Learn With Me: ReasonML, Part 2</a></p><p><a href="https://yamaceay.medium.com/learn-with-me-reasonml-part-3-fa246cc034f1">Learn With Me: ReasonML, Part 3</a></p>
