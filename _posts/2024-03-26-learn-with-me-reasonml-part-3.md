---
layout: post
title: "Learn With Me: ReasonML, Part 3"
date: 2024-03-26T23:01:34+00:00
original_url: "https://medium.com/@yamaceay/learn-with-me-reasonml-part-3-fa246cc034f1"
tags: []
excerpt: "This article requires you to have a basic understanding of ReasonML, a functional programming language which I partly covered in one of my previous articles. How to Learn a Coding Language (Fast) For "
---

{% raw %}
<p>This article requires you to have a basic understanding of ReasonML, a functional programming language which I partly covered in one of my previous articles.</p><p><a href="https://yamaceay.medium.com/how-to-learn-a-coding-language-fast-ad7a99eaf375">How to Learn a Coding Language (Fast)</a></p><p>For quick navigation, here are the other articles in the same series:</p><p><a href="https://yamaceay.medium.com/learn-with-me-reasonml-part-1-83b48d9ef694">Learn With Me: ReasonML, Part 1</a></p><p><a href="https://yamaceay.medium.com/learn-with-me-reasonml-part-2-6f704e0ded0b">Learn With Me: ReasonML, Part 2</a></p><h4>Handling Primitive Types</h4><figure><img alt="" src="https://cdn-images-1.medium.com/max/1400/1*bWlPjyo3nKKetFXqt3CCbg.png" /><figcaption>Source: Data types, pt. 1 by M. Lim, Medium</figcaption></figure><p>Mutability in ReasonML is a feature primarily used with records. Here’s how you define a mutable type that can hold any value:</p><pre><code>db.re

/* HANDLING PRIMITIVE TYPES */

// Mutability in ReasonML is a feature primarily used with records. Here&#x27;s how you define a mutable type that can hold any value:
type mut(&#x27;a) = {
  mutable value: &#x27;a,
};

// In λ-calculus, function types like f: A -&gt; B imply a transformation or proof from A to B. The functions toMut and fromMut serve as bridges between mutable and immutable types, showing they can be interchangeable:
let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;

// Using the standard implementation as a reference, you can see how it translates in practical terms:
let x = ref(0); // Equivalent to let x = toMut(0);
x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);

// ReasonML requires explicit type declarations for union types, unlike TypeScript where you might use &quot;int | null&quot;:
type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);

// Variant types in ReasonML, akin to sum types or dependent types in other languages, are exhaustive and unique, ensuring no overlap between types.

// Handling these types necessitates a switch statement, covering all possible variants for completeness:
let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};

// For pattern matching, especially when not all cases are addressed explicitly, the wildcard &quot;_&quot; can be a fallback. The &quot;when&quot; keyword allows for additional conditions in matches, offering a concise way to handle complex patterns:
let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};

// Testing different cases to demonstrate how these functions work with the defined types:
let a = toMut(A); toString(a); a.value = change(a); toString(a);
let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);

/* DATABASE STORAGE FOR DATA SCIENCE */

// Working with generic types and function handling is one thing, but let&#x27;s step into a scenario where the stakes are higher: being data scientists at a medical center, tasked with deriving basic statistics from patient data. Given a raw database in a text file format, we&#x27;ve managed to extract key information as follows:

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];

// The data&#x27;s format is row-wise with an arbitrary order, which could include duplicates, missing, or extra items. To streamline debugging, we&#x27;re aiming to cast these to string maps.

// Here&#x27;s where the Map.Make functor comes into play, allowing us to generate a StringMap keyed by strings for easier readability and manipulation, akin to handling JSON objects:
module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});

// Converting our map to a JSON-like string for debug-friendliness:
let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};

// Transitioning to a generic database format, our row-wise data gets a transformation. Here, we&#x27;re all about clarity and correctness:
let showJson = true;
let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);

// Accessing the elements becomes straightforward. Missing elements? No biggie, we handle that gracefully:
let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};

// After some exploration and analysis, key insights emerge regarding age, weight, name, and gender. These form the cornerstone of our new database signature:
type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};

// Structuring a strictly-typed database while ensuring all necessary keys are included and defaults are set for missing items:
let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);

// Finally, the database is correctly formatted. Next up, transposing this database to a column-wise format, ready for statistical analysis:
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};

// Successfully transposing our data, we&#x27;re set to dive deep into the analysis, equipped with a database that&#x27;s both comprehensive and accurately structured.
let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));

/* STATISTICS LIBRARY DEVELOPMENT */

// Venturing into building a generic statistics library, we&#x27;re focusing on versatility across different data structures. Whether dealing with Lists or Arrays, the goal is seamless integration and handling.

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
  
// The challenge lies in unpacking these varied structures into a consistent format, ideally a list of primitives, for statistical analysis. Given the evolving nature of our library, not all types are fully supported yet, leading to potential exceptions for unhandled cases.
exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};

// To ensure a smooth user experience, we wrap secToList in a function that gracefully handles exceptions, providing clear feedback rather than abrupt errors.
let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};

// Diving into the core of our library, we aim to offer basic but essential statistical functions, each designed to work with a specific type of data.

// getCounts tackles enumeration, mapping each unique string in a list to its frequency of occurrence, ideal for categorical data analysis.
let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}

// getMedian finds the middle value in a list of floats after sorting, a key measure of central tendency for quantitative data.
let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};

// getMean computes the average from a list of floats, providing a quick snapshot of your data&#x27;s central value.
let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));

// Structuring our output, we define types for summarizing string and float data, encapsulating counts for categorical data and central measures for continuous data.
type stringStats = {
  counts: list((string, int)),
};

type floatStats = {
  mean: float,
  median: float,
};

/* DATA ANALYSIS FRAMEWORK */

// Integrating complex data structures into actionable insights requires a systematic approach. We&#x27;ve established methods to deconstruct complex data into primitive lists and have statistical functions ready. The challenge now is to seamlessly connect these components.

// First, let&#x27;s categorize data types based on their analytical utility:

// - Nominal data, like colors &quot;Blue&quot; and &quot;Yellow&quot;, are distinct without a meaningful order. The mode serves as their central tendency measure.
// - Boolean data, a subset of nominal, consists of binary choices like &quot;Yes&quot; and &quot;No&quot;.
// - Ordinal data, such as ratings from 1 (&quot;Low&quot;) to 5 (&quot;High&quot;), imply order but not the uniformity of scale. Their median reflects central tendency.
// - Numeric data, representing continuous or interval data, can be fully quantified. The mean is used to express their central tendency.

// Recognizing that not all operations apply universally across data types underscores the importance of targeted analytical strategies.

// Transitioning to the implementation phase:

// The `listToFloat` function converts a list of primitives to floats, selectively allowing boolean and integer conversions based on flags:
let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};

// Converting primitives to strings while handling incompatible types by casting to floats, then stringifying, allows for flexible data interpretation:
exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};

// `getFloatStats` and `getStringStats` functions then process these lists into statistical summaries, considering the data level restrictions and debug options respectively:
let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}

// Finally, transforming primitive lists to the expected input format for statistical analysis:
let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));

// Extracting statistics becomes straightforward with prepped data:
let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);

// Now, it&#x27;s just a matter of calling the appropriate statistical function for each data type, with optional debugging for string conversions:
getStringStats(names, ~debug=true, ());
getFloatStats(weights, ~level=1, ());
getStringStats(weights, ~debug=true, ());

getFloatStats(ages, ~level=2, ());
getStringStats(ages, ~debug=true, ());

getFloatStats(males, ~level=3, ());
getStringStats(males, ~debug=true, ());

db1.re

type mut(&#x27;a) = {
  mutable value: &#x27;a,
};
// type mut(&#x27;a) = { mutable value: &#x27;a, };

db10.re

let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};
// let mapToJson: StringMap.t(prim) =&gt; string = &lt;fun&gt;;

db11.re

let showJson = true;
// let showJson: bool = true;

let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);
/* let dbGeneric: list(StringMap.t(prim)) =
  [&lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;];
*/
/*
{age: +18, male: false, name: Ada, weight: +98.5}
{age: +25, male: true, name: Ben, weight: +81.5}
{age: +45, alive: true, name: Caz, weight: +70.6}
{age: +10, male: true, name: Dan, weight: +98.5}
{male: false, name: Eve}
*/

db12.re

let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};
// let tryAccessDbGeneric: (StringMap.key, int) =&gt; prim = &lt;fun&gt;;

db13.re

type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};
// type signature = { age: prim, weight: prim, name: prim, male: prim, };

db14.re

let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);
/*
let db: list(signature) =
  [{age: D(18), weight: E(98.5), name: F(&quot;Ada&quot;), male: B(false)},
   {age: D(25), weight: E(81.5), name: F(&quot;Ben&quot;), male: B(true)},
   {age: D(45), weight: E(70.6), name: F(&quot;Caz&quot;), male: A},
   {age: D(10), weight: E(98.5), name: F(&quot;Dan&quot;), male: B(true)},
   {age: A, weight: A, name: F(&quot;Eve&quot;), male: B(false)}];
*/

db15.re

type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
/*
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
*/

db16.re

let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));
/*
let dbCol: signatureColWise =
  {ageList: [D(18), D(25), D(45), D(10), A],
   weightList: [E(98.5), E(81.5), E(70.6), E(98.5), A],
   nameList: [F(&quot;Ada&quot;), F(&quot;Ben&quot;), F(&quot;Caz&quot;), F(&quot;Dan&quot;), F(&quot;Eve&quot;)],
   maleList: [B(false), B(true), A, B(true), B(false)]};
*/

db17.re

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
/* 
type sec =
    G(prim)
  | H(list(sec))
  | I(array(sec))
  | J((string, sec))
  | K({ key: string, value: sec, });
*/

db18.re

exception Unimplemented_type(string);
// exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};
// let secToList: sec =&gt; list(prim) = &lt;fun&gt;;

db19.re

let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};
// let trySecToList: sec =&gt; list(prim) = &lt;fun&gt;;

db2.re

let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
// let toMut: &#x27;a =&gt; mut(&#x27;a) = &lt;fun&gt;;

let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;
// let fromMut: mut(&#x27;a) =&gt; &#x27;a = &lt;fun&gt;;

db20.re

let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}
// let getCounts: list(StringMap.key) =&gt; list((string, int)) = &lt;fun&gt;;

db21.re

let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};
// let getMedian: list(float) =&gt; float = &lt;fun&gt;;

db22.re

let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));
// let getMean: list(float) =&gt; float = &lt;fun&gt;;

db23.re

type stringStats = {
  counts: list((string, int)),
};
// type stringStats = { counts: list((string, int)), };

type floatStats = {
  mean: float,
  median: float,
};
// type floatStats = { mean: float, median: float, };

db24.re

let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};
/*
let listToFloat:
  (list(prim), ~boolAllowed: bool=?, ~intAllowed: bool=?, unit) =&gt; list(float) =
  &lt;fun&gt;;
*/

db25.re

exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};
// let listToString: (list(prim), ~debug: bool=?, unit) =&gt; list(string) = &lt;fun&gt;;

db26.re

let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};
// let getFloatStats: (sec, ~level: int=?, unit) =&gt; floatStats = &lt;fun&gt;;

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}
// let getStringStats: (sec, ~debug: bool=?, unit) =&gt; stringStats = &lt;fun&gt;;

db27.re

let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));
// let primListToSec: list(prim) =&gt; sec = &lt;fun&gt;;

db28.re

let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);
/*
let ages: sec = H([G((D(18))), G((D(25))), G((D(45))), G((D(10))), G(A)]);
let weights: sec =
  H([G((E(98.5))), G((E(81.5))), G((E(70.6))), G((E(98.5))), G(A)]);
let names: sec =
  H([G((F(&quot;Ada&quot;))), G((F(&quot;Ben&quot;))), G((F(&quot;Caz&quot;))), G((F(&quot;Dan&quot;))), G((F(&quot;Eve&quot;)))]);
let males: sec =
  H([G((B(false))), G((B(true))), G(A), G((B(true))), G((B(false)))]);
*/

db29.re

getStringStats(names, ~debug=true, ());
// - : stringStats = {counts: [(&quot;Ada&quot;, 1), (&quot;Ben&quot;, 1), (&quot;Caz&quot;, 1), (&quot;Dan&quot;, 1), (&quot;Eve&quot;, 1)]}

getFloatStats(weights, ~level=1, ());
// - : floatStats = {mean: 87.275, median: 90.}

getStringStats(weights, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;70.6&quot;, 1), (&quot;81.5&quot;, 1), (&quot;98.5&quot;, 2)]}

getFloatStats(ages, ~level=2, ());
// - : floatStats = {mean: 24.5, median: 21.5}

getStringStats(ages, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;10.&quot;, 1), (&quot;18.&quot;, 1), (&quot;25.&quot;, 1), (&quot;45.&quot;, 1)]}

getFloatStats(males, ~level=3, ());
// - : floatStats = {mean: 0.5, median: 0.5}

getStringStats(males, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;0.&quot;, 2), (&quot;1.&quot;, 2)]}

db3.re

let x = ref(0); // Equivalent to let x = toMut(0);
// let x: ref(int) = {contents: 0};

x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);
// - : int = 1

db4.re

type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);
// type prim = A | B(bool) | C(char) | D(int) | E(float) | F(string);

db5.re

let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};
// let change: mut(prim) =&gt; prim = &lt;fun&gt;;

db6.re

let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};
// let toString: mut(prim) =&gt; string = &lt;fun&gt;;

db7.re

let a = toMut(A); toString(a); a.value = change(a); toString(a);
// let a: mut(prim) = {value: A};
// - : string = &quot;empty&quot;
// - : string = &quot;empty&quot;

let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
// let b: mut(prim) = {value: B(false)};
// - : string = &quot;false&quot;
// - : string = &quot;true&quot;

let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
// let c: mut(prim) = {value: C(&#x27;a&#x27;)};
// - : string = &quot;a&quot;
// - : string = &quot;b&quot;

let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
// let d: mut(prim) = {value: D(0)};
// - : string = &quot;0&quot;
// - : string = &quot;+1&quot;

let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
// let e: mut(prim) = {value: E(0.)};
// - : string = &quot;0.&quot;
// - : string = &quot;+1.&quot;

let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);
// let f: mut(prim) = {value: F(&quot;Hello&quot;)};
// - : string = &quot;Hello&quot;
// - : string = &quot;Hello!&quot;

db8.re

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];
/*
let dbRaw: list(array((string, prim))) =
  [[|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(false))|],
   [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)),
     (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)),
     (&quot;alive&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|]];

*/

db9.re

module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});
// module StringMap: { ... };</code></pre><p>In λ-calculus, function types like f: A -&gt; B imply a transformation or proof from A to B. The functions toMut and fromMut serve as bridges between mutable and immutable types, showing they can be interchangeable:</p><pre><code>db.re

/* HANDLING PRIMITIVE TYPES */

// Mutability in ReasonML is a feature primarily used with records. Here&#x27;s how you define a mutable type that can hold any value:
type mut(&#x27;a) = {
  mutable value: &#x27;a,
};

// In λ-calculus, function types like f: A -&gt; B imply a transformation or proof from A to B. The functions toMut and fromMut serve as bridges between mutable and immutable types, showing they can be interchangeable:
let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;

// Using the standard implementation as a reference, you can see how it translates in practical terms:
let x = ref(0); // Equivalent to let x = toMut(0);
x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);

// ReasonML requires explicit type declarations for union types, unlike TypeScript where you might use &quot;int | null&quot;:
type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);

// Variant types in ReasonML, akin to sum types or dependent types in other languages, are exhaustive and unique, ensuring no overlap between types.

// Handling these types necessitates a switch statement, covering all possible variants for completeness:
let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};

// For pattern matching, especially when not all cases are addressed explicitly, the wildcard &quot;_&quot; can be a fallback. The &quot;when&quot; keyword allows for additional conditions in matches, offering a concise way to handle complex patterns:
let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};

// Testing different cases to demonstrate how these functions work with the defined types:
let a = toMut(A); toString(a); a.value = change(a); toString(a);
let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);

/* DATABASE STORAGE FOR DATA SCIENCE */

// Working with generic types and function handling is one thing, but let&#x27;s step into a scenario where the stakes are higher: being data scientists at a medical center, tasked with deriving basic statistics from patient data. Given a raw database in a text file format, we&#x27;ve managed to extract key information as follows:

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];

// The data&#x27;s format is row-wise with an arbitrary order, which could include duplicates, missing, or extra items. To streamline debugging, we&#x27;re aiming to cast these to string maps.

// Here&#x27;s where the Map.Make functor comes into play, allowing us to generate a StringMap keyed by strings for easier readability and manipulation, akin to handling JSON objects:
module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});

// Converting our map to a JSON-like string for debug-friendliness:
let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};

// Transitioning to a generic database format, our row-wise data gets a transformation. Here, we&#x27;re all about clarity and correctness:
let showJson = true;
let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);

// Accessing the elements becomes straightforward. Missing elements? No biggie, we handle that gracefully:
let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};

// After some exploration and analysis, key insights emerge regarding age, weight, name, and gender. These form the cornerstone of our new database signature:
type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};

// Structuring a strictly-typed database while ensuring all necessary keys are included and defaults are set for missing items:
let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);

// Finally, the database is correctly formatted. Next up, transposing this database to a column-wise format, ready for statistical analysis:
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};

// Successfully transposing our data, we&#x27;re set to dive deep into the analysis, equipped with a database that&#x27;s both comprehensive and accurately structured.
let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));

/* STATISTICS LIBRARY DEVELOPMENT */

// Venturing into building a generic statistics library, we&#x27;re focusing on versatility across different data structures. Whether dealing with Lists or Arrays, the goal is seamless integration and handling.

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
  
// The challenge lies in unpacking these varied structures into a consistent format, ideally a list of primitives, for statistical analysis. Given the evolving nature of our library, not all types are fully supported yet, leading to potential exceptions for unhandled cases.
exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};

// To ensure a smooth user experience, we wrap secToList in a function that gracefully handles exceptions, providing clear feedback rather than abrupt errors.
let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};

// Diving into the core of our library, we aim to offer basic but essential statistical functions, each designed to work with a specific type of data.

// getCounts tackles enumeration, mapping each unique string in a list to its frequency of occurrence, ideal for categorical data analysis.
let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}

// getMedian finds the middle value in a list of floats after sorting, a key measure of central tendency for quantitative data.
let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};

// getMean computes the average from a list of floats, providing a quick snapshot of your data&#x27;s central value.
let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));

// Structuring our output, we define types for summarizing string and float data, encapsulating counts for categorical data and central measures for continuous data.
type stringStats = {
  counts: list((string, int)),
};

type floatStats = {
  mean: float,
  median: float,
};

/* DATA ANALYSIS FRAMEWORK */

// Integrating complex data structures into actionable insights requires a systematic approach. We&#x27;ve established methods to deconstruct complex data into primitive lists and have statistical functions ready. The challenge now is to seamlessly connect these components.

// First, let&#x27;s categorize data types based on their analytical utility:

// - Nominal data, like colors &quot;Blue&quot; and &quot;Yellow&quot;, are distinct without a meaningful order. The mode serves as their central tendency measure.
// - Boolean data, a subset of nominal, consists of binary choices like &quot;Yes&quot; and &quot;No&quot;.
// - Ordinal data, such as ratings from 1 (&quot;Low&quot;) to 5 (&quot;High&quot;), imply order but not the uniformity of scale. Their median reflects central tendency.
// - Numeric data, representing continuous or interval data, can be fully quantified. The mean is used to express their central tendency.

// Recognizing that not all operations apply universally across data types underscores the importance of targeted analytical strategies.

// Transitioning to the implementation phase:

// The `listToFloat` function converts a list of primitives to floats, selectively allowing boolean and integer conversions based on flags:
let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};

// Converting primitives to strings while handling incompatible types by casting to floats, then stringifying, allows for flexible data interpretation:
exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};

// `getFloatStats` and `getStringStats` functions then process these lists into statistical summaries, considering the data level restrictions and debug options respectively:
let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}

// Finally, transforming primitive lists to the expected input format for statistical analysis:
let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));

// Extracting statistics becomes straightforward with prepped data:
let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);

// Now, it&#x27;s just a matter of calling the appropriate statistical function for each data type, with optional debugging for string conversions:
getStringStats(names, ~debug=true, ());
getFloatStats(weights, ~level=1, ());
getStringStats(weights, ~debug=true, ());

getFloatStats(ages, ~level=2, ());
getStringStats(ages, ~debug=true, ());

getFloatStats(males, ~level=3, ());
getStringStats(males, ~debug=true, ());

db1.re

type mut(&#x27;a) = {
  mutable value: &#x27;a,
};
// type mut(&#x27;a) = { mutable value: &#x27;a, };

db10.re

let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};
// let mapToJson: StringMap.t(prim) =&gt; string = &lt;fun&gt;;

db11.re

let showJson = true;
// let showJson: bool = true;

let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);
/* let dbGeneric: list(StringMap.t(prim)) =
  [&lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;];
*/
/*
{age: +18, male: false, name: Ada, weight: +98.5}
{age: +25, male: true, name: Ben, weight: +81.5}
{age: +45, alive: true, name: Caz, weight: +70.6}
{age: +10, male: true, name: Dan, weight: +98.5}
{male: false, name: Eve}
*/

db12.re

let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};
// let tryAccessDbGeneric: (StringMap.key, int) =&gt; prim = &lt;fun&gt;;

db13.re

type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};
// type signature = { age: prim, weight: prim, name: prim, male: prim, };

db14.re

let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);
/*
let db: list(signature) =
  [{age: D(18), weight: E(98.5), name: F(&quot;Ada&quot;), male: B(false)},
   {age: D(25), weight: E(81.5), name: F(&quot;Ben&quot;), male: B(true)},
   {age: D(45), weight: E(70.6), name: F(&quot;Caz&quot;), male: A},
   {age: D(10), weight: E(98.5), name: F(&quot;Dan&quot;), male: B(true)},
   {age: A, weight: A, name: F(&quot;Eve&quot;), male: B(false)}];
*/

db15.re

type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
/*
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
*/

db16.re

let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));
/*
let dbCol: signatureColWise =
  {ageList: [D(18), D(25), D(45), D(10), A],
   weightList: [E(98.5), E(81.5), E(70.6), E(98.5), A],
   nameList: [F(&quot;Ada&quot;), F(&quot;Ben&quot;), F(&quot;Caz&quot;), F(&quot;Dan&quot;), F(&quot;Eve&quot;)],
   maleList: [B(false), B(true), A, B(true), B(false)]};
*/

db17.re

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
/* 
type sec =
    G(prim)
  | H(list(sec))
  | I(array(sec))
  | J((string, sec))
  | K({ key: string, value: sec, });
*/

db18.re

exception Unimplemented_type(string);
// exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};
// let secToList: sec =&gt; list(prim) = &lt;fun&gt;;

db19.re

let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};
// let trySecToList: sec =&gt; list(prim) = &lt;fun&gt;;

db2.re

let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
// let toMut: &#x27;a =&gt; mut(&#x27;a) = &lt;fun&gt;;

let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;
// let fromMut: mut(&#x27;a) =&gt; &#x27;a = &lt;fun&gt;;

db20.re

let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}
// let getCounts: list(StringMap.key) =&gt; list((string, int)) = &lt;fun&gt;;

db21.re

let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};
// let getMedian: list(float) =&gt; float = &lt;fun&gt;;

db22.re

let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));
// let getMean: list(float) =&gt; float = &lt;fun&gt;;

db23.re

type stringStats = {
  counts: list((string, int)),
};
// type stringStats = { counts: list((string, int)), };

type floatStats = {
  mean: float,
  median: float,
};
// type floatStats = { mean: float, median: float, };

db24.re

let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};
/*
let listToFloat:
  (list(prim), ~boolAllowed: bool=?, ~intAllowed: bool=?, unit) =&gt; list(float) =
  &lt;fun&gt;;
*/

db25.re

exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};
// let listToString: (list(prim), ~debug: bool=?, unit) =&gt; list(string) = &lt;fun&gt;;

db26.re

let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};
// let getFloatStats: (sec, ~level: int=?, unit) =&gt; floatStats = &lt;fun&gt;;

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}
// let getStringStats: (sec, ~debug: bool=?, unit) =&gt; stringStats = &lt;fun&gt;;

db27.re

let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));
// let primListToSec: list(prim) =&gt; sec = &lt;fun&gt;;

db28.re

let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);
/*
let ages: sec = H([G((D(18))), G((D(25))), G((D(45))), G((D(10))), G(A)]);
let weights: sec =
  H([G((E(98.5))), G((E(81.5))), G((E(70.6))), G((E(98.5))), G(A)]);
let names: sec =
  H([G((F(&quot;Ada&quot;))), G((F(&quot;Ben&quot;))), G((F(&quot;Caz&quot;))), G((F(&quot;Dan&quot;))), G((F(&quot;Eve&quot;)))]);
let males: sec =
  H([G((B(false))), G((B(true))), G(A), G((B(true))), G((B(false)))]);
*/

db29.re

getStringStats(names, ~debug=true, ());
// - : stringStats = {counts: [(&quot;Ada&quot;, 1), (&quot;Ben&quot;, 1), (&quot;Caz&quot;, 1), (&quot;Dan&quot;, 1), (&quot;Eve&quot;, 1)]}

getFloatStats(weights, ~level=1, ());
// - : floatStats = {mean: 87.275, median: 90.}

getStringStats(weights, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;70.6&quot;, 1), (&quot;81.5&quot;, 1), (&quot;98.5&quot;, 2)]}

getFloatStats(ages, ~level=2, ());
// - : floatStats = {mean: 24.5, median: 21.5}

getStringStats(ages, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;10.&quot;, 1), (&quot;18.&quot;, 1), (&quot;25.&quot;, 1), (&quot;45.&quot;, 1)]}

getFloatStats(males, ~level=3, ());
// - : floatStats = {mean: 0.5, median: 0.5}

getStringStats(males, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;0.&quot;, 2), (&quot;1.&quot;, 2)]}

db3.re

let x = ref(0); // Equivalent to let x = toMut(0);
// let x: ref(int) = {contents: 0};

x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);
// - : int = 1

db4.re

type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);
// type prim = A | B(bool) | C(char) | D(int) | E(float) | F(string);

db5.re

let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};
// let change: mut(prim) =&gt; prim = &lt;fun&gt;;

db6.re

let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};
// let toString: mut(prim) =&gt; string = &lt;fun&gt;;

db7.re

let a = toMut(A); toString(a); a.value = change(a); toString(a);
// let a: mut(prim) = {value: A};
// - : string = &quot;empty&quot;
// - : string = &quot;empty&quot;

let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
// let b: mut(prim) = {value: B(false)};
// - : string = &quot;false&quot;
// - : string = &quot;true&quot;

let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
// let c: mut(prim) = {value: C(&#x27;a&#x27;)};
// - : string = &quot;a&quot;
// - : string = &quot;b&quot;

let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
// let d: mut(prim) = {value: D(0)};
// - : string = &quot;0&quot;
// - : string = &quot;+1&quot;

let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
// let e: mut(prim) = {value: E(0.)};
// - : string = &quot;0.&quot;
// - : string = &quot;+1.&quot;

let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);
// let f: mut(prim) = {value: F(&quot;Hello&quot;)};
// - : string = &quot;Hello&quot;
// - : string = &quot;Hello!&quot;

db8.re

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];
/*
let dbRaw: list(array((string, prim))) =
  [[|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(false))|],
   [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)),
     (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)),
     (&quot;alive&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|]];

*/

db9.re

module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});
// module StringMap: { ... };</code></pre><p>Using the standard implementation as a reference, you can see how it translates in practical terms:</p><pre><code>db.re

/* HANDLING PRIMITIVE TYPES */

// Mutability in ReasonML is a feature primarily used with records. Here&#x27;s how you define a mutable type that can hold any value:
type mut(&#x27;a) = {
  mutable value: &#x27;a,
};

// In λ-calculus, function types like f: A -&gt; B imply a transformation or proof from A to B. The functions toMut and fromMut serve as bridges between mutable and immutable types, showing they can be interchangeable:
let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;

// Using the standard implementation as a reference, you can see how it translates in practical terms:
let x = ref(0); // Equivalent to let x = toMut(0);
x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);

// ReasonML requires explicit type declarations for union types, unlike TypeScript where you might use &quot;int | null&quot;:
type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);

// Variant types in ReasonML, akin to sum types or dependent types in other languages, are exhaustive and unique, ensuring no overlap between types.

// Handling these types necessitates a switch statement, covering all possible variants for completeness:
let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};

// For pattern matching, especially when not all cases are addressed explicitly, the wildcard &quot;_&quot; can be a fallback. The &quot;when&quot; keyword allows for additional conditions in matches, offering a concise way to handle complex patterns:
let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};

// Testing different cases to demonstrate how these functions work with the defined types:
let a = toMut(A); toString(a); a.value = change(a); toString(a);
let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);

/* DATABASE STORAGE FOR DATA SCIENCE */

// Working with generic types and function handling is one thing, but let&#x27;s step into a scenario where the stakes are higher: being data scientists at a medical center, tasked with deriving basic statistics from patient data. Given a raw database in a text file format, we&#x27;ve managed to extract key information as follows:

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];

// The data&#x27;s format is row-wise with an arbitrary order, which could include duplicates, missing, or extra items. To streamline debugging, we&#x27;re aiming to cast these to string maps.

// Here&#x27;s where the Map.Make functor comes into play, allowing us to generate a StringMap keyed by strings for easier readability and manipulation, akin to handling JSON objects:
module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});

// Converting our map to a JSON-like string for debug-friendliness:
let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};

// Transitioning to a generic database format, our row-wise data gets a transformation. Here, we&#x27;re all about clarity and correctness:
let showJson = true;
let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);

// Accessing the elements becomes straightforward. Missing elements? No biggie, we handle that gracefully:
let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};

// After some exploration and analysis, key insights emerge regarding age, weight, name, and gender. These form the cornerstone of our new database signature:
type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};

// Structuring a strictly-typed database while ensuring all necessary keys are included and defaults are set for missing items:
let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);

// Finally, the database is correctly formatted. Next up, transposing this database to a column-wise format, ready for statistical analysis:
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};

// Successfully transposing our data, we&#x27;re set to dive deep into the analysis, equipped with a database that&#x27;s both comprehensive and accurately structured.
let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));

/* STATISTICS LIBRARY DEVELOPMENT */

// Venturing into building a generic statistics library, we&#x27;re focusing on versatility across different data structures. Whether dealing with Lists or Arrays, the goal is seamless integration and handling.

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
  
// The challenge lies in unpacking these varied structures into a consistent format, ideally a list of primitives, for statistical analysis. Given the evolving nature of our library, not all types are fully supported yet, leading to potential exceptions for unhandled cases.
exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};

// To ensure a smooth user experience, we wrap secToList in a function that gracefully handles exceptions, providing clear feedback rather than abrupt errors.
let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};

// Diving into the core of our library, we aim to offer basic but essential statistical functions, each designed to work with a specific type of data.

// getCounts tackles enumeration, mapping each unique string in a list to its frequency of occurrence, ideal for categorical data analysis.
let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}

// getMedian finds the middle value in a list of floats after sorting, a key measure of central tendency for quantitative data.
let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};

// getMean computes the average from a list of floats, providing a quick snapshot of your data&#x27;s central value.
let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));

// Structuring our output, we define types for summarizing string and float data, encapsulating counts for categorical data and central measures for continuous data.
type stringStats = {
  counts: list((string, int)),
};

type floatStats = {
  mean: float,
  median: float,
};

/* DATA ANALYSIS FRAMEWORK */

// Integrating complex data structures into actionable insights requires a systematic approach. We&#x27;ve established methods to deconstruct complex data into primitive lists and have statistical functions ready. The challenge now is to seamlessly connect these components.

// First, let&#x27;s categorize data types based on their analytical utility:

// - Nominal data, like colors &quot;Blue&quot; and &quot;Yellow&quot;, are distinct without a meaningful order. The mode serves as their central tendency measure.
// - Boolean data, a subset of nominal, consists of binary choices like &quot;Yes&quot; and &quot;No&quot;.
// - Ordinal data, such as ratings from 1 (&quot;Low&quot;) to 5 (&quot;High&quot;), imply order but not the uniformity of scale. Their median reflects central tendency.
// - Numeric data, representing continuous or interval data, can be fully quantified. The mean is used to express their central tendency.

// Recognizing that not all operations apply universally across data types underscores the importance of targeted analytical strategies.

// Transitioning to the implementation phase:

// The `listToFloat` function converts a list of primitives to floats, selectively allowing boolean and integer conversions based on flags:
let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};

// Converting primitives to strings while handling incompatible types by casting to floats, then stringifying, allows for flexible data interpretation:
exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};

// `getFloatStats` and `getStringStats` functions then process these lists into statistical summaries, considering the data level restrictions and debug options respectively:
let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}

// Finally, transforming primitive lists to the expected input format for statistical analysis:
let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));

// Extracting statistics becomes straightforward with prepped data:
let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);

// Now, it&#x27;s just a matter of calling the appropriate statistical function for each data type, with optional debugging for string conversions:
getStringStats(names, ~debug=true, ());
getFloatStats(weights, ~level=1, ());
getStringStats(weights, ~debug=true, ());

getFloatStats(ages, ~level=2, ());
getStringStats(ages, ~debug=true, ());

getFloatStats(males, ~level=3, ());
getStringStats(males, ~debug=true, ());

db1.re

type mut(&#x27;a) = {
  mutable value: &#x27;a,
};
// type mut(&#x27;a) = { mutable value: &#x27;a, };

db10.re

let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};
// let mapToJson: StringMap.t(prim) =&gt; string = &lt;fun&gt;;

db11.re

let showJson = true;
// let showJson: bool = true;

let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);
/* let dbGeneric: list(StringMap.t(prim)) =
  [&lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;];
*/
/*
{age: +18, male: false, name: Ada, weight: +98.5}
{age: +25, male: true, name: Ben, weight: +81.5}
{age: +45, alive: true, name: Caz, weight: +70.6}
{age: +10, male: true, name: Dan, weight: +98.5}
{male: false, name: Eve}
*/

db12.re

let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};
// let tryAccessDbGeneric: (StringMap.key, int) =&gt; prim = &lt;fun&gt;;

db13.re

type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};
// type signature = { age: prim, weight: prim, name: prim, male: prim, };

db14.re

let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);
/*
let db: list(signature) =
  [{age: D(18), weight: E(98.5), name: F(&quot;Ada&quot;), male: B(false)},
   {age: D(25), weight: E(81.5), name: F(&quot;Ben&quot;), male: B(true)},
   {age: D(45), weight: E(70.6), name: F(&quot;Caz&quot;), male: A},
   {age: D(10), weight: E(98.5), name: F(&quot;Dan&quot;), male: B(true)},
   {age: A, weight: A, name: F(&quot;Eve&quot;), male: B(false)}];
*/

db15.re

type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
/*
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
*/

db16.re

let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));
/*
let dbCol: signatureColWise =
  {ageList: [D(18), D(25), D(45), D(10), A],
   weightList: [E(98.5), E(81.5), E(70.6), E(98.5), A],
   nameList: [F(&quot;Ada&quot;), F(&quot;Ben&quot;), F(&quot;Caz&quot;), F(&quot;Dan&quot;), F(&quot;Eve&quot;)],
   maleList: [B(false), B(true), A, B(true), B(false)]};
*/

db17.re

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
/* 
type sec =
    G(prim)
  | H(list(sec))
  | I(array(sec))
  | J((string, sec))
  | K({ key: string, value: sec, });
*/

db18.re

exception Unimplemented_type(string);
// exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};
// let secToList: sec =&gt; list(prim) = &lt;fun&gt;;

db19.re

let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};
// let trySecToList: sec =&gt; list(prim) = &lt;fun&gt;;

db2.re

let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
// let toMut: &#x27;a =&gt; mut(&#x27;a) = &lt;fun&gt;;

let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;
// let fromMut: mut(&#x27;a) =&gt; &#x27;a = &lt;fun&gt;;

db20.re

let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}
// let getCounts: list(StringMap.key) =&gt; list((string, int)) = &lt;fun&gt;;

db21.re

let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};
// let getMedian: list(float) =&gt; float = &lt;fun&gt;;

db22.re

let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));
// let getMean: list(float) =&gt; float = &lt;fun&gt;;

db23.re

type stringStats = {
  counts: list((string, int)),
};
// type stringStats = { counts: list((string, int)), };

type floatStats = {
  mean: float,
  median: float,
};
// type floatStats = { mean: float, median: float, };

db24.re

let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};
/*
let listToFloat:
  (list(prim), ~boolAllowed: bool=?, ~intAllowed: bool=?, unit) =&gt; list(float) =
  &lt;fun&gt;;
*/

db25.re

exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};
// let listToString: (list(prim), ~debug: bool=?, unit) =&gt; list(string) = &lt;fun&gt;;

db26.re

let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};
// let getFloatStats: (sec, ~level: int=?, unit) =&gt; floatStats = &lt;fun&gt;;

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}
// let getStringStats: (sec, ~debug: bool=?, unit) =&gt; stringStats = &lt;fun&gt;;

db27.re

let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));
// let primListToSec: list(prim) =&gt; sec = &lt;fun&gt;;

db28.re

let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);
/*
let ages: sec = H([G((D(18))), G((D(25))), G((D(45))), G((D(10))), G(A)]);
let weights: sec =
  H([G((E(98.5))), G((E(81.5))), G((E(70.6))), G((E(98.5))), G(A)]);
let names: sec =
  H([G((F(&quot;Ada&quot;))), G((F(&quot;Ben&quot;))), G((F(&quot;Caz&quot;))), G((F(&quot;Dan&quot;))), G((F(&quot;Eve&quot;)))]);
let males: sec =
  H([G((B(false))), G((B(true))), G(A), G((B(true))), G((B(false)))]);
*/

db29.re

getStringStats(names, ~debug=true, ());
// - : stringStats = {counts: [(&quot;Ada&quot;, 1), (&quot;Ben&quot;, 1), (&quot;Caz&quot;, 1), (&quot;Dan&quot;, 1), (&quot;Eve&quot;, 1)]}

getFloatStats(weights, ~level=1, ());
// - : floatStats = {mean: 87.275, median: 90.}

getStringStats(weights, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;70.6&quot;, 1), (&quot;81.5&quot;, 1), (&quot;98.5&quot;, 2)]}

getFloatStats(ages, ~level=2, ());
// - : floatStats = {mean: 24.5, median: 21.5}

getStringStats(ages, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;10.&quot;, 1), (&quot;18.&quot;, 1), (&quot;25.&quot;, 1), (&quot;45.&quot;, 1)]}

getFloatStats(males, ~level=3, ());
// - : floatStats = {mean: 0.5, median: 0.5}

getStringStats(males, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;0.&quot;, 2), (&quot;1.&quot;, 2)]}

db3.re

let x = ref(0); // Equivalent to let x = toMut(0);
// let x: ref(int) = {contents: 0};

x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);
// - : int = 1

db4.re

type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);
// type prim = A | B(bool) | C(char) | D(int) | E(float) | F(string);

db5.re

let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};
// let change: mut(prim) =&gt; prim = &lt;fun&gt;;

db6.re

let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};
// let toString: mut(prim) =&gt; string = &lt;fun&gt;;

db7.re

let a = toMut(A); toString(a); a.value = change(a); toString(a);
// let a: mut(prim) = {value: A};
// - : string = &quot;empty&quot;
// - : string = &quot;empty&quot;

let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
// let b: mut(prim) = {value: B(false)};
// - : string = &quot;false&quot;
// - : string = &quot;true&quot;

let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
// let c: mut(prim) = {value: C(&#x27;a&#x27;)};
// - : string = &quot;a&quot;
// - : string = &quot;b&quot;

let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
// let d: mut(prim) = {value: D(0)};
// - : string = &quot;0&quot;
// - : string = &quot;+1&quot;

let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
// let e: mut(prim) = {value: E(0.)};
// - : string = &quot;0.&quot;
// - : string = &quot;+1.&quot;

let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);
// let f: mut(prim) = {value: F(&quot;Hello&quot;)};
// - : string = &quot;Hello&quot;
// - : string = &quot;Hello!&quot;

db8.re

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];
/*
let dbRaw: list(array((string, prim))) =
  [[|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(false))|],
   [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)),
     (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)),
     (&quot;alive&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|]];

*/

db9.re

module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});
// module StringMap: { ... };</code></pre><p>ReasonML requires explicit type declarations for union types, unlike TypeScript where you might use “int | null”:</p><pre><code>db.re

/* HANDLING PRIMITIVE TYPES */

// Mutability in ReasonML is a feature primarily used with records. Here&#x27;s how you define a mutable type that can hold any value:
type mut(&#x27;a) = {
  mutable value: &#x27;a,
};

// In λ-calculus, function types like f: A -&gt; B imply a transformation or proof from A to B. The functions toMut and fromMut serve as bridges between mutable and immutable types, showing they can be interchangeable:
let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;

// Using the standard implementation as a reference, you can see how it translates in practical terms:
let x = ref(0); // Equivalent to let x = toMut(0);
x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);

// ReasonML requires explicit type declarations for union types, unlike TypeScript where you might use &quot;int | null&quot;:
type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);

// Variant types in ReasonML, akin to sum types or dependent types in other languages, are exhaustive and unique, ensuring no overlap between types.

// Handling these types necessitates a switch statement, covering all possible variants for completeness:
let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};

// For pattern matching, especially when not all cases are addressed explicitly, the wildcard &quot;_&quot; can be a fallback. The &quot;when&quot; keyword allows for additional conditions in matches, offering a concise way to handle complex patterns:
let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};

// Testing different cases to demonstrate how these functions work with the defined types:
let a = toMut(A); toString(a); a.value = change(a); toString(a);
let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);

/* DATABASE STORAGE FOR DATA SCIENCE */

// Working with generic types and function handling is one thing, but let&#x27;s step into a scenario where the stakes are higher: being data scientists at a medical center, tasked with deriving basic statistics from patient data. Given a raw database in a text file format, we&#x27;ve managed to extract key information as follows:

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];

// The data&#x27;s format is row-wise with an arbitrary order, which could include duplicates, missing, or extra items. To streamline debugging, we&#x27;re aiming to cast these to string maps.

// Here&#x27;s where the Map.Make functor comes into play, allowing us to generate a StringMap keyed by strings for easier readability and manipulation, akin to handling JSON objects:
module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});

// Converting our map to a JSON-like string for debug-friendliness:
let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};

// Transitioning to a generic database format, our row-wise data gets a transformation. Here, we&#x27;re all about clarity and correctness:
let showJson = true;
let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);

// Accessing the elements becomes straightforward. Missing elements? No biggie, we handle that gracefully:
let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};

// After some exploration and analysis, key insights emerge regarding age, weight, name, and gender. These form the cornerstone of our new database signature:
type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};

// Structuring a strictly-typed database while ensuring all necessary keys are included and defaults are set for missing items:
let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);

// Finally, the database is correctly formatted. Next up, transposing this database to a column-wise format, ready for statistical analysis:
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};

// Successfully transposing our data, we&#x27;re set to dive deep into the analysis, equipped with a database that&#x27;s both comprehensive and accurately structured.
let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));

/* STATISTICS LIBRARY DEVELOPMENT */

// Venturing into building a generic statistics library, we&#x27;re focusing on versatility across different data structures. Whether dealing with Lists or Arrays, the goal is seamless integration and handling.

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
  
// The challenge lies in unpacking these varied structures into a consistent format, ideally a list of primitives, for statistical analysis. Given the evolving nature of our library, not all types are fully supported yet, leading to potential exceptions for unhandled cases.
exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};

// To ensure a smooth user experience, we wrap secToList in a function that gracefully handles exceptions, providing clear feedback rather than abrupt errors.
let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};

// Diving into the core of our library, we aim to offer basic but essential statistical functions, each designed to work with a specific type of data.

// getCounts tackles enumeration, mapping each unique string in a list to its frequency of occurrence, ideal for categorical data analysis.
let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}

// getMedian finds the middle value in a list of floats after sorting, a key measure of central tendency for quantitative data.
let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};

// getMean computes the average from a list of floats, providing a quick snapshot of your data&#x27;s central value.
let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));

// Structuring our output, we define types for summarizing string and float data, encapsulating counts for categorical data and central measures for continuous data.
type stringStats = {
  counts: list((string, int)),
};

type floatStats = {
  mean: float,
  median: float,
};

/* DATA ANALYSIS FRAMEWORK */

// Integrating complex data structures into actionable insights requires a systematic approach. We&#x27;ve established methods to deconstruct complex data into primitive lists and have statistical functions ready. The challenge now is to seamlessly connect these components.

// First, let&#x27;s categorize data types based on their analytical utility:

// - Nominal data, like colors &quot;Blue&quot; and &quot;Yellow&quot;, are distinct without a meaningful order. The mode serves as their central tendency measure.
// - Boolean data, a subset of nominal, consists of binary choices like &quot;Yes&quot; and &quot;No&quot;.
// - Ordinal data, such as ratings from 1 (&quot;Low&quot;) to 5 (&quot;High&quot;), imply order but not the uniformity of scale. Their median reflects central tendency.
// - Numeric data, representing continuous or interval data, can be fully quantified. The mean is used to express their central tendency.

// Recognizing that not all operations apply universally across data types underscores the importance of targeted analytical strategies.

// Transitioning to the implementation phase:

// The `listToFloat` function converts a list of primitives to floats, selectively allowing boolean and integer conversions based on flags:
let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};

// Converting primitives to strings while handling incompatible types by casting to floats, then stringifying, allows for flexible data interpretation:
exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};

// `getFloatStats` and `getStringStats` functions then process these lists into statistical summaries, considering the data level restrictions and debug options respectively:
let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}

// Finally, transforming primitive lists to the expected input format for statistical analysis:
let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));

// Extracting statistics becomes straightforward with prepped data:
let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);

// Now, it&#x27;s just a matter of calling the appropriate statistical function for each data type, with optional debugging for string conversions:
getStringStats(names, ~debug=true, ());
getFloatStats(weights, ~level=1, ());
getStringStats(weights, ~debug=true, ());

getFloatStats(ages, ~level=2, ());
getStringStats(ages, ~debug=true, ());

getFloatStats(males, ~level=3, ());
getStringStats(males, ~debug=true, ());

db1.re

type mut(&#x27;a) = {
  mutable value: &#x27;a,
};
// type mut(&#x27;a) = { mutable value: &#x27;a, };

db10.re

let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};
// let mapToJson: StringMap.t(prim) =&gt; string = &lt;fun&gt;;

db11.re

let showJson = true;
// let showJson: bool = true;

let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);
/* let dbGeneric: list(StringMap.t(prim)) =
  [&lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;];
*/
/*
{age: +18, male: false, name: Ada, weight: +98.5}
{age: +25, male: true, name: Ben, weight: +81.5}
{age: +45, alive: true, name: Caz, weight: +70.6}
{age: +10, male: true, name: Dan, weight: +98.5}
{male: false, name: Eve}
*/

db12.re

let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};
// let tryAccessDbGeneric: (StringMap.key, int) =&gt; prim = &lt;fun&gt;;

db13.re

type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};
// type signature = { age: prim, weight: prim, name: prim, male: prim, };

db14.re

let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);
/*
let db: list(signature) =
  [{age: D(18), weight: E(98.5), name: F(&quot;Ada&quot;), male: B(false)},
   {age: D(25), weight: E(81.5), name: F(&quot;Ben&quot;), male: B(true)},
   {age: D(45), weight: E(70.6), name: F(&quot;Caz&quot;), male: A},
   {age: D(10), weight: E(98.5), name: F(&quot;Dan&quot;), male: B(true)},
   {age: A, weight: A, name: F(&quot;Eve&quot;), male: B(false)}];
*/

db15.re

type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
/*
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
*/

db16.re

let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));
/*
let dbCol: signatureColWise =
  {ageList: [D(18), D(25), D(45), D(10), A],
   weightList: [E(98.5), E(81.5), E(70.6), E(98.5), A],
   nameList: [F(&quot;Ada&quot;), F(&quot;Ben&quot;), F(&quot;Caz&quot;), F(&quot;Dan&quot;), F(&quot;Eve&quot;)],
   maleList: [B(false), B(true), A, B(true), B(false)]};
*/

db17.re

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
/* 
type sec =
    G(prim)
  | H(list(sec))
  | I(array(sec))
  | J((string, sec))
  | K({ key: string, value: sec, });
*/

db18.re

exception Unimplemented_type(string);
// exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};
// let secToList: sec =&gt; list(prim) = &lt;fun&gt;;

db19.re

let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};
// let trySecToList: sec =&gt; list(prim) = &lt;fun&gt;;

db2.re

let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
// let toMut: &#x27;a =&gt; mut(&#x27;a) = &lt;fun&gt;;

let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;
// let fromMut: mut(&#x27;a) =&gt; &#x27;a = &lt;fun&gt;;

db20.re

let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}
// let getCounts: list(StringMap.key) =&gt; list((string, int)) = &lt;fun&gt;;

db21.re

let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};
// let getMedian: list(float) =&gt; float = &lt;fun&gt;;

db22.re

let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));
// let getMean: list(float) =&gt; float = &lt;fun&gt;;

db23.re

type stringStats = {
  counts: list((string, int)),
};
// type stringStats = { counts: list((string, int)), };

type floatStats = {
  mean: float,
  median: float,
};
// type floatStats = { mean: float, median: float, };

db24.re

let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};
/*
let listToFloat:
  (list(prim), ~boolAllowed: bool=?, ~intAllowed: bool=?, unit) =&gt; list(float) =
  &lt;fun&gt;;
*/

db25.re

exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};
// let listToString: (list(prim), ~debug: bool=?, unit) =&gt; list(string) = &lt;fun&gt;;

db26.re

let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};
// let getFloatStats: (sec, ~level: int=?, unit) =&gt; floatStats = &lt;fun&gt;;

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}
// let getStringStats: (sec, ~debug: bool=?, unit) =&gt; stringStats = &lt;fun&gt;;

db27.re

let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));
// let primListToSec: list(prim) =&gt; sec = &lt;fun&gt;;

db28.re

let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);
/*
let ages: sec = H([G((D(18))), G((D(25))), G((D(45))), G((D(10))), G(A)]);
let weights: sec =
  H([G((E(98.5))), G((E(81.5))), G((E(70.6))), G((E(98.5))), G(A)]);
let names: sec =
  H([G((F(&quot;Ada&quot;))), G((F(&quot;Ben&quot;))), G((F(&quot;Caz&quot;))), G((F(&quot;Dan&quot;))), G((F(&quot;Eve&quot;)))]);
let males: sec =
  H([G((B(false))), G((B(true))), G(A), G((B(true))), G((B(false)))]);
*/

db29.re

getStringStats(names, ~debug=true, ());
// - : stringStats = {counts: [(&quot;Ada&quot;, 1), (&quot;Ben&quot;, 1), (&quot;Caz&quot;, 1), (&quot;Dan&quot;, 1), (&quot;Eve&quot;, 1)]}

getFloatStats(weights, ~level=1, ());
// - : floatStats = {mean: 87.275, median: 90.}

getStringStats(weights, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;70.6&quot;, 1), (&quot;81.5&quot;, 1), (&quot;98.5&quot;, 2)]}

getFloatStats(ages, ~level=2, ());
// - : floatStats = {mean: 24.5, median: 21.5}

getStringStats(ages, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;10.&quot;, 1), (&quot;18.&quot;, 1), (&quot;25.&quot;, 1), (&quot;45.&quot;, 1)]}

getFloatStats(males, ~level=3, ());
// - : floatStats = {mean: 0.5, median: 0.5}

getStringStats(males, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;0.&quot;, 2), (&quot;1.&quot;, 2)]}

db3.re

let x = ref(0); // Equivalent to let x = toMut(0);
// let x: ref(int) = {contents: 0};

x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);
// - : int = 1

db4.re

type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);
// type prim = A | B(bool) | C(char) | D(int) | E(float) | F(string);

db5.re

let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};
// let change: mut(prim) =&gt; prim = &lt;fun&gt;;

db6.re

let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};
// let toString: mut(prim) =&gt; string = &lt;fun&gt;;

db7.re

let a = toMut(A); toString(a); a.value = change(a); toString(a);
// let a: mut(prim) = {value: A};
// - : string = &quot;empty&quot;
// - : string = &quot;empty&quot;

let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
// let b: mut(prim) = {value: B(false)};
// - : string = &quot;false&quot;
// - : string = &quot;true&quot;

let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
// let c: mut(prim) = {value: C(&#x27;a&#x27;)};
// - : string = &quot;a&quot;
// - : string = &quot;b&quot;

let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
// let d: mut(prim) = {value: D(0)};
// - : string = &quot;0&quot;
// - : string = &quot;+1&quot;

let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
// let e: mut(prim) = {value: E(0.)};
// - : string = &quot;0.&quot;
// - : string = &quot;+1.&quot;

let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);
// let f: mut(prim) = {value: F(&quot;Hello&quot;)};
// - : string = &quot;Hello&quot;
// - : string = &quot;Hello!&quot;

db8.re

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];
/*
let dbRaw: list(array((string, prim))) =
  [[|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(false))|],
   [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)),
     (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)),
     (&quot;alive&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|]];

*/

db9.re

module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});
// module StringMap: { ... };</code></pre><p>Variant types in ReasonML, akin to sum types or dependent types in other languages, are exhaustive and unique, ensuring no overlap between types.</p><p>Handling these types necessitates a switch statement, covering all possible variants for completeness:</p><pre><code>db.re

/* HANDLING PRIMITIVE TYPES */

// Mutability in ReasonML is a feature primarily used with records. Here&#x27;s how you define a mutable type that can hold any value:
type mut(&#x27;a) = {
  mutable value: &#x27;a,
};

// In λ-calculus, function types like f: A -&gt; B imply a transformation or proof from A to B. The functions toMut and fromMut serve as bridges between mutable and immutable types, showing they can be interchangeable:
let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;

// Using the standard implementation as a reference, you can see how it translates in practical terms:
let x = ref(0); // Equivalent to let x = toMut(0);
x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);

// ReasonML requires explicit type declarations for union types, unlike TypeScript where you might use &quot;int | null&quot;:
type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);

// Variant types in ReasonML, akin to sum types or dependent types in other languages, are exhaustive and unique, ensuring no overlap between types.

// Handling these types necessitates a switch statement, covering all possible variants for completeness:
let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};

// For pattern matching, especially when not all cases are addressed explicitly, the wildcard &quot;_&quot; can be a fallback. The &quot;when&quot; keyword allows for additional conditions in matches, offering a concise way to handle complex patterns:
let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};

// Testing different cases to demonstrate how these functions work with the defined types:
let a = toMut(A); toString(a); a.value = change(a); toString(a);
let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);

/* DATABASE STORAGE FOR DATA SCIENCE */

// Working with generic types and function handling is one thing, but let&#x27;s step into a scenario where the stakes are higher: being data scientists at a medical center, tasked with deriving basic statistics from patient data. Given a raw database in a text file format, we&#x27;ve managed to extract key information as follows:

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];

// The data&#x27;s format is row-wise with an arbitrary order, which could include duplicates, missing, or extra items. To streamline debugging, we&#x27;re aiming to cast these to string maps.

// Here&#x27;s where the Map.Make functor comes into play, allowing us to generate a StringMap keyed by strings for easier readability and manipulation, akin to handling JSON objects:
module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});

// Converting our map to a JSON-like string for debug-friendliness:
let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};

// Transitioning to a generic database format, our row-wise data gets a transformation. Here, we&#x27;re all about clarity and correctness:
let showJson = true;
let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);

// Accessing the elements becomes straightforward. Missing elements? No biggie, we handle that gracefully:
let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};

// After some exploration and analysis, key insights emerge regarding age, weight, name, and gender. These form the cornerstone of our new database signature:
type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};

// Structuring a strictly-typed database while ensuring all necessary keys are included and defaults are set for missing items:
let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);

// Finally, the database is correctly formatted. Next up, transposing this database to a column-wise format, ready for statistical analysis:
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};

// Successfully transposing our data, we&#x27;re set to dive deep into the analysis, equipped with a database that&#x27;s both comprehensive and accurately structured.
let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));

/* STATISTICS LIBRARY DEVELOPMENT */

// Venturing into building a generic statistics library, we&#x27;re focusing on versatility across different data structures. Whether dealing with Lists or Arrays, the goal is seamless integration and handling.

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
  
// The challenge lies in unpacking these varied structures into a consistent format, ideally a list of primitives, for statistical analysis. Given the evolving nature of our library, not all types are fully supported yet, leading to potential exceptions for unhandled cases.
exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};

// To ensure a smooth user experience, we wrap secToList in a function that gracefully handles exceptions, providing clear feedback rather than abrupt errors.
let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};

// Diving into the core of our library, we aim to offer basic but essential statistical functions, each designed to work with a specific type of data.

// getCounts tackles enumeration, mapping each unique string in a list to its frequency of occurrence, ideal for categorical data analysis.
let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}

// getMedian finds the middle value in a list of floats after sorting, a key measure of central tendency for quantitative data.
let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};

// getMean computes the average from a list of floats, providing a quick snapshot of your data&#x27;s central value.
let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));

// Structuring our output, we define types for summarizing string and float data, encapsulating counts for categorical data and central measures for continuous data.
type stringStats = {
  counts: list((string, int)),
};

type floatStats = {
  mean: float,
  median: float,
};

/* DATA ANALYSIS FRAMEWORK */

// Integrating complex data structures into actionable insights requires a systematic approach. We&#x27;ve established methods to deconstruct complex data into primitive lists and have statistical functions ready. The challenge now is to seamlessly connect these components.

// First, let&#x27;s categorize data types based on their analytical utility:

// - Nominal data, like colors &quot;Blue&quot; and &quot;Yellow&quot;, are distinct without a meaningful order. The mode serves as their central tendency measure.
// - Boolean data, a subset of nominal, consists of binary choices like &quot;Yes&quot; and &quot;No&quot;.
// - Ordinal data, such as ratings from 1 (&quot;Low&quot;) to 5 (&quot;High&quot;), imply order but not the uniformity of scale. Their median reflects central tendency.
// - Numeric data, representing continuous or interval data, can be fully quantified. The mean is used to express their central tendency.

// Recognizing that not all operations apply universally across data types underscores the importance of targeted analytical strategies.

// Transitioning to the implementation phase:

// The `listToFloat` function converts a list of primitives to floats, selectively allowing boolean and integer conversions based on flags:
let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};

// Converting primitives to strings while handling incompatible types by casting to floats, then stringifying, allows for flexible data interpretation:
exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};

// `getFloatStats` and `getStringStats` functions then process these lists into statistical summaries, considering the data level restrictions and debug options respectively:
let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}

// Finally, transforming primitive lists to the expected input format for statistical analysis:
let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));

// Extracting statistics becomes straightforward with prepped data:
let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);

// Now, it&#x27;s just a matter of calling the appropriate statistical function for each data type, with optional debugging for string conversions:
getStringStats(names, ~debug=true, ());
getFloatStats(weights, ~level=1, ());
getStringStats(weights, ~debug=true, ());

getFloatStats(ages, ~level=2, ());
getStringStats(ages, ~debug=true, ());

getFloatStats(males, ~level=3, ());
getStringStats(males, ~debug=true, ());

db1.re

type mut(&#x27;a) = {
  mutable value: &#x27;a,
};
// type mut(&#x27;a) = { mutable value: &#x27;a, };

db10.re

let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};
// let mapToJson: StringMap.t(prim) =&gt; string = &lt;fun&gt;;

db11.re

let showJson = true;
// let showJson: bool = true;

let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);
/* let dbGeneric: list(StringMap.t(prim)) =
  [&lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;];
*/
/*
{age: +18, male: false, name: Ada, weight: +98.5}
{age: +25, male: true, name: Ben, weight: +81.5}
{age: +45, alive: true, name: Caz, weight: +70.6}
{age: +10, male: true, name: Dan, weight: +98.5}
{male: false, name: Eve}
*/

db12.re

let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};
// let tryAccessDbGeneric: (StringMap.key, int) =&gt; prim = &lt;fun&gt;;

db13.re

type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};
// type signature = { age: prim, weight: prim, name: prim, male: prim, };

db14.re

let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);
/*
let db: list(signature) =
  [{age: D(18), weight: E(98.5), name: F(&quot;Ada&quot;), male: B(false)},
   {age: D(25), weight: E(81.5), name: F(&quot;Ben&quot;), male: B(true)},
   {age: D(45), weight: E(70.6), name: F(&quot;Caz&quot;), male: A},
   {age: D(10), weight: E(98.5), name: F(&quot;Dan&quot;), male: B(true)},
   {age: A, weight: A, name: F(&quot;Eve&quot;), male: B(false)}];
*/

db15.re

type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
/*
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
*/

db16.re

let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));
/*
let dbCol: signatureColWise =
  {ageList: [D(18), D(25), D(45), D(10), A],
   weightList: [E(98.5), E(81.5), E(70.6), E(98.5), A],
   nameList: [F(&quot;Ada&quot;), F(&quot;Ben&quot;), F(&quot;Caz&quot;), F(&quot;Dan&quot;), F(&quot;Eve&quot;)],
   maleList: [B(false), B(true), A, B(true), B(false)]};
*/

db17.re

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
/* 
type sec =
    G(prim)
  | H(list(sec))
  | I(array(sec))
  | J((string, sec))
  | K({ key: string, value: sec, });
*/

db18.re

exception Unimplemented_type(string);
// exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};
// let secToList: sec =&gt; list(prim) = &lt;fun&gt;;

db19.re

let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};
// let trySecToList: sec =&gt; list(prim) = &lt;fun&gt;;

db2.re

let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
// let toMut: &#x27;a =&gt; mut(&#x27;a) = &lt;fun&gt;;

let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;
// let fromMut: mut(&#x27;a) =&gt; &#x27;a = &lt;fun&gt;;

db20.re

let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}
// let getCounts: list(StringMap.key) =&gt; list((string, int)) = &lt;fun&gt;;

db21.re

let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};
// let getMedian: list(float) =&gt; float = &lt;fun&gt;;

db22.re

let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));
// let getMean: list(float) =&gt; float = &lt;fun&gt;;

db23.re

type stringStats = {
  counts: list((string, int)),
};
// type stringStats = { counts: list((string, int)), };

type floatStats = {
  mean: float,
  median: float,
};
// type floatStats = { mean: float, median: float, };

db24.re

let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};
/*
let listToFloat:
  (list(prim), ~boolAllowed: bool=?, ~intAllowed: bool=?, unit) =&gt; list(float) =
  &lt;fun&gt;;
*/

db25.re

exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};
// let listToString: (list(prim), ~debug: bool=?, unit) =&gt; list(string) = &lt;fun&gt;;

db26.re

let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};
// let getFloatStats: (sec, ~level: int=?, unit) =&gt; floatStats = &lt;fun&gt;;

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}
// let getStringStats: (sec, ~debug: bool=?, unit) =&gt; stringStats = &lt;fun&gt;;

db27.re

let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));
// let primListToSec: list(prim) =&gt; sec = &lt;fun&gt;;

db28.re

let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);
/*
let ages: sec = H([G((D(18))), G((D(25))), G((D(45))), G((D(10))), G(A)]);
let weights: sec =
  H([G((E(98.5))), G((E(81.5))), G((E(70.6))), G((E(98.5))), G(A)]);
let names: sec =
  H([G((F(&quot;Ada&quot;))), G((F(&quot;Ben&quot;))), G((F(&quot;Caz&quot;))), G((F(&quot;Dan&quot;))), G((F(&quot;Eve&quot;)))]);
let males: sec =
  H([G((B(false))), G((B(true))), G(A), G((B(true))), G((B(false)))]);
*/

db29.re

getStringStats(names, ~debug=true, ());
// - : stringStats = {counts: [(&quot;Ada&quot;, 1), (&quot;Ben&quot;, 1), (&quot;Caz&quot;, 1), (&quot;Dan&quot;, 1), (&quot;Eve&quot;, 1)]}

getFloatStats(weights, ~level=1, ());
// - : floatStats = {mean: 87.275, median: 90.}

getStringStats(weights, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;70.6&quot;, 1), (&quot;81.5&quot;, 1), (&quot;98.5&quot;, 2)]}

getFloatStats(ages, ~level=2, ());
// - : floatStats = {mean: 24.5, median: 21.5}

getStringStats(ages, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;10.&quot;, 1), (&quot;18.&quot;, 1), (&quot;25.&quot;, 1), (&quot;45.&quot;, 1)]}

getFloatStats(males, ~level=3, ());
// - : floatStats = {mean: 0.5, median: 0.5}

getStringStats(males, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;0.&quot;, 2), (&quot;1.&quot;, 2)]}

db3.re

let x = ref(0); // Equivalent to let x = toMut(0);
// let x: ref(int) = {contents: 0};

x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);
// - : int = 1

db4.re

type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);
// type prim = A | B(bool) | C(char) | D(int) | E(float) | F(string);

db5.re

let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};
// let change: mut(prim) =&gt; prim = &lt;fun&gt;;

db6.re

let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};
// let toString: mut(prim) =&gt; string = &lt;fun&gt;;

db7.re

let a = toMut(A); toString(a); a.value = change(a); toString(a);
// let a: mut(prim) = {value: A};
// - : string = &quot;empty&quot;
// - : string = &quot;empty&quot;

let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
// let b: mut(prim) = {value: B(false)};
// - : string = &quot;false&quot;
// - : string = &quot;true&quot;

let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
// let c: mut(prim) = {value: C(&#x27;a&#x27;)};
// - : string = &quot;a&quot;
// - : string = &quot;b&quot;

let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
// let d: mut(prim) = {value: D(0)};
// - : string = &quot;0&quot;
// - : string = &quot;+1&quot;

let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
// let e: mut(prim) = {value: E(0.)};
// - : string = &quot;0.&quot;
// - : string = &quot;+1.&quot;

let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);
// let f: mut(prim) = {value: F(&quot;Hello&quot;)};
// - : string = &quot;Hello&quot;
// - : string = &quot;Hello!&quot;

db8.re

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];
/*
let dbRaw: list(array((string, prim))) =
  [[|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(false))|],
   [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)),
     (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)),
     (&quot;alive&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|]];

*/

db9.re

module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});
// module StringMap: { ... };</code></pre><p>For pattern matching, especially when not all cases are addressed explicitly, the wildcard “_” can be a fallback. The “when” keyword allows for additional conditions in matches, offering a concise way to handle complex patterns:</p><pre><code>db.re

/* HANDLING PRIMITIVE TYPES */

// Mutability in ReasonML is a feature primarily used with records. Here&#x27;s how you define a mutable type that can hold any value:
type mut(&#x27;a) = {
  mutable value: &#x27;a,
};

// In λ-calculus, function types like f: A -&gt; B imply a transformation or proof from A to B. The functions toMut and fromMut serve as bridges between mutable and immutable types, showing they can be interchangeable:
let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;

// Using the standard implementation as a reference, you can see how it translates in practical terms:
let x = ref(0); // Equivalent to let x = toMut(0);
x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);

// ReasonML requires explicit type declarations for union types, unlike TypeScript where you might use &quot;int | null&quot;:
type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);

// Variant types in ReasonML, akin to sum types or dependent types in other languages, are exhaustive and unique, ensuring no overlap between types.

// Handling these types necessitates a switch statement, covering all possible variants for completeness:
let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};

// For pattern matching, especially when not all cases are addressed explicitly, the wildcard &quot;_&quot; can be a fallback. The &quot;when&quot; keyword allows for additional conditions in matches, offering a concise way to handle complex patterns:
let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};

// Testing different cases to demonstrate how these functions work with the defined types:
let a = toMut(A); toString(a); a.value = change(a); toString(a);
let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);

/* DATABASE STORAGE FOR DATA SCIENCE */

// Working with generic types and function handling is one thing, but let&#x27;s step into a scenario where the stakes are higher: being data scientists at a medical center, tasked with deriving basic statistics from patient data. Given a raw database in a text file format, we&#x27;ve managed to extract key information as follows:

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];

// The data&#x27;s format is row-wise with an arbitrary order, which could include duplicates, missing, or extra items. To streamline debugging, we&#x27;re aiming to cast these to string maps.

// Here&#x27;s where the Map.Make functor comes into play, allowing us to generate a StringMap keyed by strings for easier readability and manipulation, akin to handling JSON objects:
module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});

// Converting our map to a JSON-like string for debug-friendliness:
let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};

// Transitioning to a generic database format, our row-wise data gets a transformation. Here, we&#x27;re all about clarity and correctness:
let showJson = true;
let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);

// Accessing the elements becomes straightforward. Missing elements? No biggie, we handle that gracefully:
let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};

// After some exploration and analysis, key insights emerge regarding age, weight, name, and gender. These form the cornerstone of our new database signature:
type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};

// Structuring a strictly-typed database while ensuring all necessary keys are included and defaults are set for missing items:
let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);

// Finally, the database is correctly formatted. Next up, transposing this database to a column-wise format, ready for statistical analysis:
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};

// Successfully transposing our data, we&#x27;re set to dive deep into the analysis, equipped with a database that&#x27;s both comprehensive and accurately structured.
let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));

/* STATISTICS LIBRARY DEVELOPMENT */

// Venturing into building a generic statistics library, we&#x27;re focusing on versatility across different data structures. Whether dealing with Lists or Arrays, the goal is seamless integration and handling.

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
  
// The challenge lies in unpacking these varied structures into a consistent format, ideally a list of primitives, for statistical analysis. Given the evolving nature of our library, not all types are fully supported yet, leading to potential exceptions for unhandled cases.
exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};

// To ensure a smooth user experience, we wrap secToList in a function that gracefully handles exceptions, providing clear feedback rather than abrupt errors.
let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};

// Diving into the core of our library, we aim to offer basic but essential statistical functions, each designed to work with a specific type of data.

// getCounts tackles enumeration, mapping each unique string in a list to its frequency of occurrence, ideal for categorical data analysis.
let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}

// getMedian finds the middle value in a list of floats after sorting, a key measure of central tendency for quantitative data.
let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};

// getMean computes the average from a list of floats, providing a quick snapshot of your data&#x27;s central value.
let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));

// Structuring our output, we define types for summarizing string and float data, encapsulating counts for categorical data and central measures for continuous data.
type stringStats = {
  counts: list((string, int)),
};

type floatStats = {
  mean: float,
  median: float,
};

/* DATA ANALYSIS FRAMEWORK */

// Integrating complex data structures into actionable insights requires a systematic approach. We&#x27;ve established methods to deconstruct complex data into primitive lists and have statistical functions ready. The challenge now is to seamlessly connect these components.

// First, let&#x27;s categorize data types based on their analytical utility:

// - Nominal data, like colors &quot;Blue&quot; and &quot;Yellow&quot;, are distinct without a meaningful order. The mode serves as their central tendency measure.
// - Boolean data, a subset of nominal, consists of binary choices like &quot;Yes&quot; and &quot;No&quot;.
// - Ordinal data, such as ratings from 1 (&quot;Low&quot;) to 5 (&quot;High&quot;), imply order but not the uniformity of scale. Their median reflects central tendency.
// - Numeric data, representing continuous or interval data, can be fully quantified. The mean is used to express their central tendency.

// Recognizing that not all operations apply universally across data types underscores the importance of targeted analytical strategies.

// Transitioning to the implementation phase:

// The `listToFloat` function converts a list of primitives to floats, selectively allowing boolean and integer conversions based on flags:
let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};

// Converting primitives to strings while handling incompatible types by casting to floats, then stringifying, allows for flexible data interpretation:
exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};

// `getFloatStats` and `getStringStats` functions then process these lists into statistical summaries, considering the data level restrictions and debug options respectively:
let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}

// Finally, transforming primitive lists to the expected input format for statistical analysis:
let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));

// Extracting statistics becomes straightforward with prepped data:
let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);

// Now, it&#x27;s just a matter of calling the appropriate statistical function for each data type, with optional debugging for string conversions:
getStringStats(names, ~debug=true, ());
getFloatStats(weights, ~level=1, ());
getStringStats(weights, ~debug=true, ());

getFloatStats(ages, ~level=2, ());
getStringStats(ages, ~debug=true, ());

getFloatStats(males, ~level=3, ());
getStringStats(males, ~debug=true, ());

db1.re

type mut(&#x27;a) = {
  mutable value: &#x27;a,
};
// type mut(&#x27;a) = { mutable value: &#x27;a, };

db10.re

let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};
// let mapToJson: StringMap.t(prim) =&gt; string = &lt;fun&gt;;

db11.re

let showJson = true;
// let showJson: bool = true;

let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);
/* let dbGeneric: list(StringMap.t(prim)) =
  [&lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;];
*/
/*
{age: +18, male: false, name: Ada, weight: +98.5}
{age: +25, male: true, name: Ben, weight: +81.5}
{age: +45, alive: true, name: Caz, weight: +70.6}
{age: +10, male: true, name: Dan, weight: +98.5}
{male: false, name: Eve}
*/

db12.re

let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};
// let tryAccessDbGeneric: (StringMap.key, int) =&gt; prim = &lt;fun&gt;;

db13.re

type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};
// type signature = { age: prim, weight: prim, name: prim, male: prim, };

db14.re

let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);
/*
let db: list(signature) =
  [{age: D(18), weight: E(98.5), name: F(&quot;Ada&quot;), male: B(false)},
   {age: D(25), weight: E(81.5), name: F(&quot;Ben&quot;), male: B(true)},
   {age: D(45), weight: E(70.6), name: F(&quot;Caz&quot;), male: A},
   {age: D(10), weight: E(98.5), name: F(&quot;Dan&quot;), male: B(true)},
   {age: A, weight: A, name: F(&quot;Eve&quot;), male: B(false)}];
*/

db15.re

type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
/*
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
*/

db16.re

let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));
/*
let dbCol: signatureColWise =
  {ageList: [D(18), D(25), D(45), D(10), A],
   weightList: [E(98.5), E(81.5), E(70.6), E(98.5), A],
   nameList: [F(&quot;Ada&quot;), F(&quot;Ben&quot;), F(&quot;Caz&quot;), F(&quot;Dan&quot;), F(&quot;Eve&quot;)],
   maleList: [B(false), B(true), A, B(true), B(false)]};
*/

db17.re

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
/* 
type sec =
    G(prim)
  | H(list(sec))
  | I(array(sec))
  | J((string, sec))
  | K({ key: string, value: sec, });
*/

db18.re

exception Unimplemented_type(string);
// exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};
// let secToList: sec =&gt; list(prim) = &lt;fun&gt;;

db19.re

let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};
// let trySecToList: sec =&gt; list(prim) = &lt;fun&gt;;

db2.re

let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
// let toMut: &#x27;a =&gt; mut(&#x27;a) = &lt;fun&gt;;

let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;
// let fromMut: mut(&#x27;a) =&gt; &#x27;a = &lt;fun&gt;;

db20.re

let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}
// let getCounts: list(StringMap.key) =&gt; list((string, int)) = &lt;fun&gt;;

db21.re

let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};
// let getMedian: list(float) =&gt; float = &lt;fun&gt;;

db22.re

let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));
// let getMean: list(float) =&gt; float = &lt;fun&gt;;

db23.re

type stringStats = {
  counts: list((string, int)),
};
// type stringStats = { counts: list((string, int)), };

type floatStats = {
  mean: float,
  median: float,
};
// type floatStats = { mean: float, median: float, };

db24.re

let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};
/*
let listToFloat:
  (list(prim), ~boolAllowed: bool=?, ~intAllowed: bool=?, unit) =&gt; list(float) =
  &lt;fun&gt;;
*/

db25.re

exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};
// let listToString: (list(prim), ~debug: bool=?, unit) =&gt; list(string) = &lt;fun&gt;;

db26.re

let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};
// let getFloatStats: (sec, ~level: int=?, unit) =&gt; floatStats = &lt;fun&gt;;

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}
// let getStringStats: (sec, ~debug: bool=?, unit) =&gt; stringStats = &lt;fun&gt;;

db27.re

let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));
// let primListToSec: list(prim) =&gt; sec = &lt;fun&gt;;

db28.re

let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);
/*
let ages: sec = H([G((D(18))), G((D(25))), G((D(45))), G((D(10))), G(A)]);
let weights: sec =
  H([G((E(98.5))), G((E(81.5))), G((E(70.6))), G((E(98.5))), G(A)]);
let names: sec =
  H([G((F(&quot;Ada&quot;))), G((F(&quot;Ben&quot;))), G((F(&quot;Caz&quot;))), G((F(&quot;Dan&quot;))), G((F(&quot;Eve&quot;)))]);
let males: sec =
  H([G((B(false))), G((B(true))), G(A), G((B(true))), G((B(false)))]);
*/

db29.re

getStringStats(names, ~debug=true, ());
// - : stringStats = {counts: [(&quot;Ada&quot;, 1), (&quot;Ben&quot;, 1), (&quot;Caz&quot;, 1), (&quot;Dan&quot;, 1), (&quot;Eve&quot;, 1)]}

getFloatStats(weights, ~level=1, ());
// - : floatStats = {mean: 87.275, median: 90.}

getStringStats(weights, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;70.6&quot;, 1), (&quot;81.5&quot;, 1), (&quot;98.5&quot;, 2)]}

getFloatStats(ages, ~level=2, ());
// - : floatStats = {mean: 24.5, median: 21.5}

getStringStats(ages, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;10.&quot;, 1), (&quot;18.&quot;, 1), (&quot;25.&quot;, 1), (&quot;45.&quot;, 1)]}

getFloatStats(males, ~level=3, ());
// - : floatStats = {mean: 0.5, median: 0.5}

getStringStats(males, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;0.&quot;, 2), (&quot;1.&quot;, 2)]}

db3.re

let x = ref(0); // Equivalent to let x = toMut(0);
// let x: ref(int) = {contents: 0};

x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);
// - : int = 1

db4.re

type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);
// type prim = A | B(bool) | C(char) | D(int) | E(float) | F(string);

db5.re

let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};
// let change: mut(prim) =&gt; prim = &lt;fun&gt;;

db6.re

let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};
// let toString: mut(prim) =&gt; string = &lt;fun&gt;;

db7.re

let a = toMut(A); toString(a); a.value = change(a); toString(a);
// let a: mut(prim) = {value: A};
// - : string = &quot;empty&quot;
// - : string = &quot;empty&quot;

let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
// let b: mut(prim) = {value: B(false)};
// - : string = &quot;false&quot;
// - : string = &quot;true&quot;

let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
// let c: mut(prim) = {value: C(&#x27;a&#x27;)};
// - : string = &quot;a&quot;
// - : string = &quot;b&quot;

let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
// let d: mut(prim) = {value: D(0)};
// - : string = &quot;0&quot;
// - : string = &quot;+1&quot;

let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
// let e: mut(prim) = {value: E(0.)};
// - : string = &quot;0.&quot;
// - : string = &quot;+1.&quot;

let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);
// let f: mut(prim) = {value: F(&quot;Hello&quot;)};
// - : string = &quot;Hello&quot;
// - : string = &quot;Hello!&quot;

db8.re

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];
/*
let dbRaw: list(array((string, prim))) =
  [[|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(false))|],
   [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)),
     (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)),
     (&quot;alive&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|]];

*/

db9.re

module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});
// module StringMap: { ... };</code></pre><p>Testing different cases to demonstrate how these functions work with the defined types:</p><pre><code>db.re

/* HANDLING PRIMITIVE TYPES */

// Mutability in ReasonML is a feature primarily used with records. Here&#x27;s how you define a mutable type that can hold any value:
type mut(&#x27;a) = {
  mutable value: &#x27;a,
};

// In λ-calculus, function types like f: A -&gt; B imply a transformation or proof from A to B. The functions toMut and fromMut serve as bridges between mutable and immutable types, showing they can be interchangeable:
let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;

// Using the standard implementation as a reference, you can see how it translates in practical terms:
let x = ref(0); // Equivalent to let x = toMut(0);
x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);

// ReasonML requires explicit type declarations for union types, unlike TypeScript where you might use &quot;int | null&quot;:
type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);

// Variant types in ReasonML, akin to sum types or dependent types in other languages, are exhaustive and unique, ensuring no overlap between types.

// Handling these types necessitates a switch statement, covering all possible variants for completeness:
let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};

// For pattern matching, especially when not all cases are addressed explicitly, the wildcard &quot;_&quot; can be a fallback. The &quot;when&quot; keyword allows for additional conditions in matches, offering a concise way to handle complex patterns:
let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};

// Testing different cases to demonstrate how these functions work with the defined types:
let a = toMut(A); toString(a); a.value = change(a); toString(a);
let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);

/* DATABASE STORAGE FOR DATA SCIENCE */

// Working with generic types and function handling is one thing, but let&#x27;s step into a scenario where the stakes are higher: being data scientists at a medical center, tasked with deriving basic statistics from patient data. Given a raw database in a text file format, we&#x27;ve managed to extract key information as follows:

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];

// The data&#x27;s format is row-wise with an arbitrary order, which could include duplicates, missing, or extra items. To streamline debugging, we&#x27;re aiming to cast these to string maps.

// Here&#x27;s where the Map.Make functor comes into play, allowing us to generate a StringMap keyed by strings for easier readability and manipulation, akin to handling JSON objects:
module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});

// Converting our map to a JSON-like string for debug-friendliness:
let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};

// Transitioning to a generic database format, our row-wise data gets a transformation. Here, we&#x27;re all about clarity and correctness:
let showJson = true;
let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);

// Accessing the elements becomes straightforward. Missing elements? No biggie, we handle that gracefully:
let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};

// After some exploration and analysis, key insights emerge regarding age, weight, name, and gender. These form the cornerstone of our new database signature:
type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};

// Structuring a strictly-typed database while ensuring all necessary keys are included and defaults are set for missing items:
let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);

// Finally, the database is correctly formatted. Next up, transposing this database to a column-wise format, ready for statistical analysis:
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};

// Successfully transposing our data, we&#x27;re set to dive deep into the analysis, equipped with a database that&#x27;s both comprehensive and accurately structured.
let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));

/* STATISTICS LIBRARY DEVELOPMENT */

// Venturing into building a generic statistics library, we&#x27;re focusing on versatility across different data structures. Whether dealing with Lists or Arrays, the goal is seamless integration and handling.

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
  
// The challenge lies in unpacking these varied structures into a consistent format, ideally a list of primitives, for statistical analysis. Given the evolving nature of our library, not all types are fully supported yet, leading to potential exceptions for unhandled cases.
exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};

// To ensure a smooth user experience, we wrap secToList in a function that gracefully handles exceptions, providing clear feedback rather than abrupt errors.
let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};

// Diving into the core of our library, we aim to offer basic but essential statistical functions, each designed to work with a specific type of data.

// getCounts tackles enumeration, mapping each unique string in a list to its frequency of occurrence, ideal for categorical data analysis.
let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}

// getMedian finds the middle value in a list of floats after sorting, a key measure of central tendency for quantitative data.
let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};

// getMean computes the average from a list of floats, providing a quick snapshot of your data&#x27;s central value.
let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));

// Structuring our output, we define types for summarizing string and float data, encapsulating counts for categorical data and central measures for continuous data.
type stringStats = {
  counts: list((string, int)),
};

type floatStats = {
  mean: float,
  median: float,
};

/* DATA ANALYSIS FRAMEWORK */

// Integrating complex data structures into actionable insights requires a systematic approach. We&#x27;ve established methods to deconstruct complex data into primitive lists and have statistical functions ready. The challenge now is to seamlessly connect these components.

// First, let&#x27;s categorize data types based on their analytical utility:

// - Nominal data, like colors &quot;Blue&quot; and &quot;Yellow&quot;, are distinct without a meaningful order. The mode serves as their central tendency measure.
// - Boolean data, a subset of nominal, consists of binary choices like &quot;Yes&quot; and &quot;No&quot;.
// - Ordinal data, such as ratings from 1 (&quot;Low&quot;) to 5 (&quot;High&quot;), imply order but not the uniformity of scale. Their median reflects central tendency.
// - Numeric data, representing continuous or interval data, can be fully quantified. The mean is used to express their central tendency.

// Recognizing that not all operations apply universally across data types underscores the importance of targeted analytical strategies.

// Transitioning to the implementation phase:

// The `listToFloat` function converts a list of primitives to floats, selectively allowing boolean and integer conversions based on flags:
let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};

// Converting primitives to strings while handling incompatible types by casting to floats, then stringifying, allows for flexible data interpretation:
exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};

// `getFloatStats` and `getStringStats` functions then process these lists into statistical summaries, considering the data level restrictions and debug options respectively:
let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}

// Finally, transforming primitive lists to the expected input format for statistical analysis:
let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));

// Extracting statistics becomes straightforward with prepped data:
let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);

// Now, it&#x27;s just a matter of calling the appropriate statistical function for each data type, with optional debugging for string conversions:
getStringStats(names, ~debug=true, ());
getFloatStats(weights, ~level=1, ());
getStringStats(weights, ~debug=true, ());

getFloatStats(ages, ~level=2, ());
getStringStats(ages, ~debug=true, ());

getFloatStats(males, ~level=3, ());
getStringStats(males, ~debug=true, ());

db1.re

type mut(&#x27;a) = {
  mutable value: &#x27;a,
};
// type mut(&#x27;a) = { mutable value: &#x27;a, };

db10.re

let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};
// let mapToJson: StringMap.t(prim) =&gt; string = &lt;fun&gt;;

db11.re

let showJson = true;
// let showJson: bool = true;

let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);
/* let dbGeneric: list(StringMap.t(prim)) =
  [&lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;];
*/
/*
{age: +18, male: false, name: Ada, weight: +98.5}
{age: +25, male: true, name: Ben, weight: +81.5}
{age: +45, alive: true, name: Caz, weight: +70.6}
{age: +10, male: true, name: Dan, weight: +98.5}
{male: false, name: Eve}
*/

db12.re

let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};
// let tryAccessDbGeneric: (StringMap.key, int) =&gt; prim = &lt;fun&gt;;

db13.re

type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};
// type signature = { age: prim, weight: prim, name: prim, male: prim, };

db14.re

let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);
/*
let db: list(signature) =
  [{age: D(18), weight: E(98.5), name: F(&quot;Ada&quot;), male: B(false)},
   {age: D(25), weight: E(81.5), name: F(&quot;Ben&quot;), male: B(true)},
   {age: D(45), weight: E(70.6), name: F(&quot;Caz&quot;), male: A},
   {age: D(10), weight: E(98.5), name: F(&quot;Dan&quot;), male: B(true)},
   {age: A, weight: A, name: F(&quot;Eve&quot;), male: B(false)}];
*/

db15.re

type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
/*
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
*/

db16.re

let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));
/*
let dbCol: signatureColWise =
  {ageList: [D(18), D(25), D(45), D(10), A],
   weightList: [E(98.5), E(81.5), E(70.6), E(98.5), A],
   nameList: [F(&quot;Ada&quot;), F(&quot;Ben&quot;), F(&quot;Caz&quot;), F(&quot;Dan&quot;), F(&quot;Eve&quot;)],
   maleList: [B(false), B(true), A, B(true), B(false)]};
*/

db17.re

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
/* 
type sec =
    G(prim)
  | H(list(sec))
  | I(array(sec))
  | J((string, sec))
  | K({ key: string, value: sec, });
*/

db18.re

exception Unimplemented_type(string);
// exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};
// let secToList: sec =&gt; list(prim) = &lt;fun&gt;;

db19.re

let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};
// let trySecToList: sec =&gt; list(prim) = &lt;fun&gt;;

db2.re

let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
// let toMut: &#x27;a =&gt; mut(&#x27;a) = &lt;fun&gt;;

let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;
// let fromMut: mut(&#x27;a) =&gt; &#x27;a = &lt;fun&gt;;

db20.re

let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}
// let getCounts: list(StringMap.key) =&gt; list((string, int)) = &lt;fun&gt;;

db21.re

let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};
// let getMedian: list(float) =&gt; float = &lt;fun&gt;;

db22.re

let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));
// let getMean: list(float) =&gt; float = &lt;fun&gt;;

db23.re

type stringStats = {
  counts: list((string, int)),
};
// type stringStats = { counts: list((string, int)), };

type floatStats = {
  mean: float,
  median: float,
};
// type floatStats = { mean: float, median: float, };

db24.re

let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};
/*
let listToFloat:
  (list(prim), ~boolAllowed: bool=?, ~intAllowed: bool=?, unit) =&gt; list(float) =
  &lt;fun&gt;;
*/

db25.re

exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};
// let listToString: (list(prim), ~debug: bool=?, unit) =&gt; list(string) = &lt;fun&gt;;

db26.re

let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};
// let getFloatStats: (sec, ~level: int=?, unit) =&gt; floatStats = &lt;fun&gt;;

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}
// let getStringStats: (sec, ~debug: bool=?, unit) =&gt; stringStats = &lt;fun&gt;;

db27.re

let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));
// let primListToSec: list(prim) =&gt; sec = &lt;fun&gt;;

db28.re

let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);
/*
let ages: sec = H([G((D(18))), G((D(25))), G((D(45))), G((D(10))), G(A)]);
let weights: sec =
  H([G((E(98.5))), G((E(81.5))), G((E(70.6))), G((E(98.5))), G(A)]);
let names: sec =
  H([G((F(&quot;Ada&quot;))), G((F(&quot;Ben&quot;))), G((F(&quot;Caz&quot;))), G((F(&quot;Dan&quot;))), G((F(&quot;Eve&quot;)))]);
let males: sec =
  H([G((B(false))), G((B(true))), G(A), G((B(true))), G((B(false)))]);
*/

db29.re

getStringStats(names, ~debug=true, ());
// - : stringStats = {counts: [(&quot;Ada&quot;, 1), (&quot;Ben&quot;, 1), (&quot;Caz&quot;, 1), (&quot;Dan&quot;, 1), (&quot;Eve&quot;, 1)]}

getFloatStats(weights, ~level=1, ());
// - : floatStats = {mean: 87.275, median: 90.}

getStringStats(weights, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;70.6&quot;, 1), (&quot;81.5&quot;, 1), (&quot;98.5&quot;, 2)]}

getFloatStats(ages, ~level=2, ());
// - : floatStats = {mean: 24.5, median: 21.5}

getStringStats(ages, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;10.&quot;, 1), (&quot;18.&quot;, 1), (&quot;25.&quot;, 1), (&quot;45.&quot;, 1)]}

getFloatStats(males, ~level=3, ());
// - : floatStats = {mean: 0.5, median: 0.5}

getStringStats(males, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;0.&quot;, 2), (&quot;1.&quot;, 2)]}

db3.re

let x = ref(0); // Equivalent to let x = toMut(0);
// let x: ref(int) = {contents: 0};

x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);
// - : int = 1

db4.re

type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);
// type prim = A | B(bool) | C(char) | D(int) | E(float) | F(string);

db5.re

let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};
// let change: mut(prim) =&gt; prim = &lt;fun&gt;;

db6.re

let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};
// let toString: mut(prim) =&gt; string = &lt;fun&gt;;

db7.re

let a = toMut(A); toString(a); a.value = change(a); toString(a);
// let a: mut(prim) = {value: A};
// - : string = &quot;empty&quot;
// - : string = &quot;empty&quot;

let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
// let b: mut(prim) = {value: B(false)};
// - : string = &quot;false&quot;
// - : string = &quot;true&quot;

let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
// let c: mut(prim) = {value: C(&#x27;a&#x27;)};
// - : string = &quot;a&quot;
// - : string = &quot;b&quot;

let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
// let d: mut(prim) = {value: D(0)};
// - : string = &quot;0&quot;
// - : string = &quot;+1&quot;

let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
// let e: mut(prim) = {value: E(0.)};
// - : string = &quot;0.&quot;
// - : string = &quot;+1.&quot;

let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);
// let f: mut(prim) = {value: F(&quot;Hello&quot;)};
// - : string = &quot;Hello&quot;
// - : string = &quot;Hello!&quot;

db8.re

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];
/*
let dbRaw: list(array((string, prim))) =
  [[|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(false))|],
   [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)),
     (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)),
     (&quot;alive&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|]];

*/

db9.re

module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});
// module StringMap: { ... };</code></pre><h4>Database Storage</h4><figure><img alt="" src="https://cdn-images-1.medium.com/max/1400/1*CecK2UFWyRtRbPbNH9pLaQ.png" /><figcaption>Source: Python Pandas DataFrame, geeksforgeeks.org</figcaption></figure><p>Working with generic types and function handling is one thing, but let’s step into a scenario where the stakes are higher: being data scientists at a medical center, tasked with deriving basic statistics from patient data. Given a raw database in a text file format, we’ve managed to extract key information as follows:</p><pre><code>db.re

/* HANDLING PRIMITIVE TYPES */

// Mutability in ReasonML is a feature primarily used with records. Here&#x27;s how you define a mutable type that can hold any value:
type mut(&#x27;a) = {
  mutable value: &#x27;a,
};

// In λ-calculus, function types like f: A -&gt; B imply a transformation or proof from A to B. The functions toMut and fromMut serve as bridges between mutable and immutable types, showing they can be interchangeable:
let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;

// Using the standard implementation as a reference, you can see how it translates in practical terms:
let x = ref(0); // Equivalent to let x = toMut(0);
x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);

// ReasonML requires explicit type declarations for union types, unlike TypeScript where you might use &quot;int | null&quot;:
type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);

// Variant types in ReasonML, akin to sum types or dependent types in other languages, are exhaustive and unique, ensuring no overlap between types.

// Handling these types necessitates a switch statement, covering all possible variants for completeness:
let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};

// For pattern matching, especially when not all cases are addressed explicitly, the wildcard &quot;_&quot; can be a fallback. The &quot;when&quot; keyword allows for additional conditions in matches, offering a concise way to handle complex patterns:
let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};

// Testing different cases to demonstrate how these functions work with the defined types:
let a = toMut(A); toString(a); a.value = change(a); toString(a);
let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);

/* DATABASE STORAGE FOR DATA SCIENCE */

// Working with generic types and function handling is one thing, but let&#x27;s step into a scenario where the stakes are higher: being data scientists at a medical center, tasked with deriving basic statistics from patient data. Given a raw database in a text file format, we&#x27;ve managed to extract key information as follows:

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];

// The data&#x27;s format is row-wise with an arbitrary order, which could include duplicates, missing, or extra items. To streamline debugging, we&#x27;re aiming to cast these to string maps.

// Here&#x27;s where the Map.Make functor comes into play, allowing us to generate a StringMap keyed by strings for easier readability and manipulation, akin to handling JSON objects:
module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});

// Converting our map to a JSON-like string for debug-friendliness:
let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};

// Transitioning to a generic database format, our row-wise data gets a transformation. Here, we&#x27;re all about clarity and correctness:
let showJson = true;
let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);

// Accessing the elements becomes straightforward. Missing elements? No biggie, we handle that gracefully:
let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};

// After some exploration and analysis, key insights emerge regarding age, weight, name, and gender. These form the cornerstone of our new database signature:
type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};

// Structuring a strictly-typed database while ensuring all necessary keys are included and defaults are set for missing items:
let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);

// Finally, the database is correctly formatted. Next up, transposing this database to a column-wise format, ready for statistical analysis:
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};

// Successfully transposing our data, we&#x27;re set to dive deep into the analysis, equipped with a database that&#x27;s both comprehensive and accurately structured.
let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));

/* STATISTICS LIBRARY DEVELOPMENT */

// Venturing into building a generic statistics library, we&#x27;re focusing on versatility across different data structures. Whether dealing with Lists or Arrays, the goal is seamless integration and handling.

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
  
// The challenge lies in unpacking these varied structures into a consistent format, ideally a list of primitives, for statistical analysis. Given the evolving nature of our library, not all types are fully supported yet, leading to potential exceptions for unhandled cases.
exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};

// To ensure a smooth user experience, we wrap secToList in a function that gracefully handles exceptions, providing clear feedback rather than abrupt errors.
let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};

// Diving into the core of our library, we aim to offer basic but essential statistical functions, each designed to work with a specific type of data.

// getCounts tackles enumeration, mapping each unique string in a list to its frequency of occurrence, ideal for categorical data analysis.
let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}

// getMedian finds the middle value in a list of floats after sorting, a key measure of central tendency for quantitative data.
let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};

// getMean computes the average from a list of floats, providing a quick snapshot of your data&#x27;s central value.
let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));

// Structuring our output, we define types for summarizing string and float data, encapsulating counts for categorical data and central measures for continuous data.
type stringStats = {
  counts: list((string, int)),
};

type floatStats = {
  mean: float,
  median: float,
};

/* DATA ANALYSIS FRAMEWORK */

// Integrating complex data structures into actionable insights requires a systematic approach. We&#x27;ve established methods to deconstruct complex data into primitive lists and have statistical functions ready. The challenge now is to seamlessly connect these components.

// First, let&#x27;s categorize data types based on their analytical utility:

// - Nominal data, like colors &quot;Blue&quot; and &quot;Yellow&quot;, are distinct without a meaningful order. The mode serves as their central tendency measure.
// - Boolean data, a subset of nominal, consists of binary choices like &quot;Yes&quot; and &quot;No&quot;.
// - Ordinal data, such as ratings from 1 (&quot;Low&quot;) to 5 (&quot;High&quot;), imply order but not the uniformity of scale. Their median reflects central tendency.
// - Numeric data, representing continuous or interval data, can be fully quantified. The mean is used to express their central tendency.

// Recognizing that not all operations apply universally across data types underscores the importance of targeted analytical strategies.

// Transitioning to the implementation phase:

// The `listToFloat` function converts a list of primitives to floats, selectively allowing boolean and integer conversions based on flags:
let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};

// Converting primitives to strings while handling incompatible types by casting to floats, then stringifying, allows for flexible data interpretation:
exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};

// `getFloatStats` and `getStringStats` functions then process these lists into statistical summaries, considering the data level restrictions and debug options respectively:
let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}

// Finally, transforming primitive lists to the expected input format for statistical analysis:
let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));

// Extracting statistics becomes straightforward with prepped data:
let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);

// Now, it&#x27;s just a matter of calling the appropriate statistical function for each data type, with optional debugging for string conversions:
getStringStats(names, ~debug=true, ());
getFloatStats(weights, ~level=1, ());
getStringStats(weights, ~debug=true, ());

getFloatStats(ages, ~level=2, ());
getStringStats(ages, ~debug=true, ());

getFloatStats(males, ~level=3, ());
getStringStats(males, ~debug=true, ());

db1.re

type mut(&#x27;a) = {
  mutable value: &#x27;a,
};
// type mut(&#x27;a) = { mutable value: &#x27;a, };

db10.re

let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};
// let mapToJson: StringMap.t(prim) =&gt; string = &lt;fun&gt;;

db11.re

let showJson = true;
// let showJson: bool = true;

let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);
/* let dbGeneric: list(StringMap.t(prim)) =
  [&lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;];
*/
/*
{age: +18, male: false, name: Ada, weight: +98.5}
{age: +25, male: true, name: Ben, weight: +81.5}
{age: +45, alive: true, name: Caz, weight: +70.6}
{age: +10, male: true, name: Dan, weight: +98.5}
{male: false, name: Eve}
*/

db12.re

let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};
// let tryAccessDbGeneric: (StringMap.key, int) =&gt; prim = &lt;fun&gt;;

db13.re

type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};
// type signature = { age: prim, weight: prim, name: prim, male: prim, };

db14.re

let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);
/*
let db: list(signature) =
  [{age: D(18), weight: E(98.5), name: F(&quot;Ada&quot;), male: B(false)},
   {age: D(25), weight: E(81.5), name: F(&quot;Ben&quot;), male: B(true)},
   {age: D(45), weight: E(70.6), name: F(&quot;Caz&quot;), male: A},
   {age: D(10), weight: E(98.5), name: F(&quot;Dan&quot;), male: B(true)},
   {age: A, weight: A, name: F(&quot;Eve&quot;), male: B(false)}];
*/

db15.re

type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
/*
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
*/

db16.re

let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));
/*
let dbCol: signatureColWise =
  {ageList: [D(18), D(25), D(45), D(10), A],
   weightList: [E(98.5), E(81.5), E(70.6), E(98.5), A],
   nameList: [F(&quot;Ada&quot;), F(&quot;Ben&quot;), F(&quot;Caz&quot;), F(&quot;Dan&quot;), F(&quot;Eve&quot;)],
   maleList: [B(false), B(true), A, B(true), B(false)]};
*/

db17.re

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
/* 
type sec =
    G(prim)
  | H(list(sec))
  | I(array(sec))
  | J((string, sec))
  | K({ key: string, value: sec, });
*/

db18.re

exception Unimplemented_type(string);
// exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};
// let secToList: sec =&gt; list(prim) = &lt;fun&gt;;

db19.re

let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};
// let trySecToList: sec =&gt; list(prim) = &lt;fun&gt;;

db2.re

let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
// let toMut: &#x27;a =&gt; mut(&#x27;a) = &lt;fun&gt;;

let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;
// let fromMut: mut(&#x27;a) =&gt; &#x27;a = &lt;fun&gt;;

db20.re

let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}
// let getCounts: list(StringMap.key) =&gt; list((string, int)) = &lt;fun&gt;;

db21.re

let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};
// let getMedian: list(float) =&gt; float = &lt;fun&gt;;

db22.re

let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));
// let getMean: list(float) =&gt; float = &lt;fun&gt;;

db23.re

type stringStats = {
  counts: list((string, int)),
};
// type stringStats = { counts: list((string, int)), };

type floatStats = {
  mean: float,
  median: float,
};
// type floatStats = { mean: float, median: float, };

db24.re

let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};
/*
let listToFloat:
  (list(prim), ~boolAllowed: bool=?, ~intAllowed: bool=?, unit) =&gt; list(float) =
  &lt;fun&gt;;
*/

db25.re

exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};
// let listToString: (list(prim), ~debug: bool=?, unit) =&gt; list(string) = &lt;fun&gt;;

db26.re

let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};
// let getFloatStats: (sec, ~level: int=?, unit) =&gt; floatStats = &lt;fun&gt;;

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}
// let getStringStats: (sec, ~debug: bool=?, unit) =&gt; stringStats = &lt;fun&gt;;

db27.re

let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));
// let primListToSec: list(prim) =&gt; sec = &lt;fun&gt;;

db28.re

let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);
/*
let ages: sec = H([G((D(18))), G((D(25))), G((D(45))), G((D(10))), G(A)]);
let weights: sec =
  H([G((E(98.5))), G((E(81.5))), G((E(70.6))), G((E(98.5))), G(A)]);
let names: sec =
  H([G((F(&quot;Ada&quot;))), G((F(&quot;Ben&quot;))), G((F(&quot;Caz&quot;))), G((F(&quot;Dan&quot;))), G((F(&quot;Eve&quot;)))]);
let males: sec =
  H([G((B(false))), G((B(true))), G(A), G((B(true))), G((B(false)))]);
*/

db29.re

getStringStats(names, ~debug=true, ());
// - : stringStats = {counts: [(&quot;Ada&quot;, 1), (&quot;Ben&quot;, 1), (&quot;Caz&quot;, 1), (&quot;Dan&quot;, 1), (&quot;Eve&quot;, 1)]}

getFloatStats(weights, ~level=1, ());
// - : floatStats = {mean: 87.275, median: 90.}

getStringStats(weights, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;70.6&quot;, 1), (&quot;81.5&quot;, 1), (&quot;98.5&quot;, 2)]}

getFloatStats(ages, ~level=2, ());
// - : floatStats = {mean: 24.5, median: 21.5}

getStringStats(ages, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;10.&quot;, 1), (&quot;18.&quot;, 1), (&quot;25.&quot;, 1), (&quot;45.&quot;, 1)]}

getFloatStats(males, ~level=3, ());
// - : floatStats = {mean: 0.5, median: 0.5}

getStringStats(males, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;0.&quot;, 2), (&quot;1.&quot;, 2)]}

db3.re

let x = ref(0); // Equivalent to let x = toMut(0);
// let x: ref(int) = {contents: 0};

x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);
// - : int = 1

db4.re

type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);
// type prim = A | B(bool) | C(char) | D(int) | E(float) | F(string);

db5.re

let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};
// let change: mut(prim) =&gt; prim = &lt;fun&gt;;

db6.re

let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};
// let toString: mut(prim) =&gt; string = &lt;fun&gt;;

db7.re

let a = toMut(A); toString(a); a.value = change(a); toString(a);
// let a: mut(prim) = {value: A};
// - : string = &quot;empty&quot;
// - : string = &quot;empty&quot;

let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
// let b: mut(prim) = {value: B(false)};
// - : string = &quot;false&quot;
// - : string = &quot;true&quot;

let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
// let c: mut(prim) = {value: C(&#x27;a&#x27;)};
// - : string = &quot;a&quot;
// - : string = &quot;b&quot;

let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
// let d: mut(prim) = {value: D(0)};
// - : string = &quot;0&quot;
// - : string = &quot;+1&quot;

let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
// let e: mut(prim) = {value: E(0.)};
// - : string = &quot;0.&quot;
// - : string = &quot;+1.&quot;

let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);
// let f: mut(prim) = {value: F(&quot;Hello&quot;)};
// - : string = &quot;Hello&quot;
// - : string = &quot;Hello!&quot;

db8.re

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];
/*
let dbRaw: list(array((string, prim))) =
  [[|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(false))|],
   [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)),
     (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)),
     (&quot;alive&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|]];

*/

db9.re

module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});
// module StringMap: { ... };</code></pre><p>The data’s format is row-wise with an arbitrary order, which could include duplicates, missing, or extra items. To streamline debugging, we’re aiming to cast these to string maps.</p><p>Here’s where the Map.Make functor comes into play, allowing us to generate a StringMap keyed by strings for easier readability and manipulation, akin to handling JSON objects:</p><pre><code>db.re

/* HANDLING PRIMITIVE TYPES */

// Mutability in ReasonML is a feature primarily used with records. Here&#x27;s how you define a mutable type that can hold any value:
type mut(&#x27;a) = {
  mutable value: &#x27;a,
};

// In λ-calculus, function types like f: A -&gt; B imply a transformation or proof from A to B. The functions toMut and fromMut serve as bridges between mutable and immutable types, showing they can be interchangeable:
let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;

// Using the standard implementation as a reference, you can see how it translates in practical terms:
let x = ref(0); // Equivalent to let x = toMut(0);
x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);

// ReasonML requires explicit type declarations for union types, unlike TypeScript where you might use &quot;int | null&quot;:
type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);

// Variant types in ReasonML, akin to sum types or dependent types in other languages, are exhaustive and unique, ensuring no overlap between types.

// Handling these types necessitates a switch statement, covering all possible variants for completeness:
let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};

// For pattern matching, especially when not all cases are addressed explicitly, the wildcard &quot;_&quot; can be a fallback. The &quot;when&quot; keyword allows for additional conditions in matches, offering a concise way to handle complex patterns:
let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};

// Testing different cases to demonstrate how these functions work with the defined types:
let a = toMut(A); toString(a); a.value = change(a); toString(a);
let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);

/* DATABASE STORAGE FOR DATA SCIENCE */

// Working with generic types and function handling is one thing, but let&#x27;s step into a scenario where the stakes are higher: being data scientists at a medical center, tasked with deriving basic statistics from patient data. Given a raw database in a text file format, we&#x27;ve managed to extract key information as follows:

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];

// The data&#x27;s format is row-wise with an arbitrary order, which could include duplicates, missing, or extra items. To streamline debugging, we&#x27;re aiming to cast these to string maps.

// Here&#x27;s where the Map.Make functor comes into play, allowing us to generate a StringMap keyed by strings for easier readability and manipulation, akin to handling JSON objects:
module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});

// Converting our map to a JSON-like string for debug-friendliness:
let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};

// Transitioning to a generic database format, our row-wise data gets a transformation. Here, we&#x27;re all about clarity and correctness:
let showJson = true;
let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);

// Accessing the elements becomes straightforward. Missing elements? No biggie, we handle that gracefully:
let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};

// After some exploration and analysis, key insights emerge regarding age, weight, name, and gender. These form the cornerstone of our new database signature:
type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};

// Structuring a strictly-typed database while ensuring all necessary keys are included and defaults are set for missing items:
let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);

// Finally, the database is correctly formatted. Next up, transposing this database to a column-wise format, ready for statistical analysis:
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};

// Successfully transposing our data, we&#x27;re set to dive deep into the analysis, equipped with a database that&#x27;s both comprehensive and accurately structured.
let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));

/* STATISTICS LIBRARY DEVELOPMENT */

// Venturing into building a generic statistics library, we&#x27;re focusing on versatility across different data structures. Whether dealing with Lists or Arrays, the goal is seamless integration and handling.

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
  
// The challenge lies in unpacking these varied structures into a consistent format, ideally a list of primitives, for statistical analysis. Given the evolving nature of our library, not all types are fully supported yet, leading to potential exceptions for unhandled cases.
exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};

// To ensure a smooth user experience, we wrap secToList in a function that gracefully handles exceptions, providing clear feedback rather than abrupt errors.
let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};

// Diving into the core of our library, we aim to offer basic but essential statistical functions, each designed to work with a specific type of data.

// getCounts tackles enumeration, mapping each unique string in a list to its frequency of occurrence, ideal for categorical data analysis.
let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}

// getMedian finds the middle value in a list of floats after sorting, a key measure of central tendency for quantitative data.
let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};

// getMean computes the average from a list of floats, providing a quick snapshot of your data&#x27;s central value.
let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));

// Structuring our output, we define types for summarizing string and float data, encapsulating counts for categorical data and central measures for continuous data.
type stringStats = {
  counts: list((string, int)),
};

type floatStats = {
  mean: float,
  median: float,
};

/* DATA ANALYSIS FRAMEWORK */

// Integrating complex data structures into actionable insights requires a systematic approach. We&#x27;ve established methods to deconstruct complex data into primitive lists and have statistical functions ready. The challenge now is to seamlessly connect these components.

// First, let&#x27;s categorize data types based on their analytical utility:

// - Nominal data, like colors &quot;Blue&quot; and &quot;Yellow&quot;, are distinct without a meaningful order. The mode serves as their central tendency measure.
// - Boolean data, a subset of nominal, consists of binary choices like &quot;Yes&quot; and &quot;No&quot;.
// - Ordinal data, such as ratings from 1 (&quot;Low&quot;) to 5 (&quot;High&quot;), imply order but not the uniformity of scale. Their median reflects central tendency.
// - Numeric data, representing continuous or interval data, can be fully quantified. The mean is used to express their central tendency.

// Recognizing that not all operations apply universally across data types underscores the importance of targeted analytical strategies.

// Transitioning to the implementation phase:

// The `listToFloat` function converts a list of primitives to floats, selectively allowing boolean and integer conversions based on flags:
let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};

// Converting primitives to strings while handling incompatible types by casting to floats, then stringifying, allows for flexible data interpretation:
exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};

// `getFloatStats` and `getStringStats` functions then process these lists into statistical summaries, considering the data level restrictions and debug options respectively:
let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}

// Finally, transforming primitive lists to the expected input format for statistical analysis:
let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));

// Extracting statistics becomes straightforward with prepped data:
let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);

// Now, it&#x27;s just a matter of calling the appropriate statistical function for each data type, with optional debugging for string conversions:
getStringStats(names, ~debug=true, ());
getFloatStats(weights, ~level=1, ());
getStringStats(weights, ~debug=true, ());

getFloatStats(ages, ~level=2, ());
getStringStats(ages, ~debug=true, ());

getFloatStats(males, ~level=3, ());
getStringStats(males, ~debug=true, ());

db1.re

type mut(&#x27;a) = {
  mutable value: &#x27;a,
};
// type mut(&#x27;a) = { mutable value: &#x27;a, };

db10.re

let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};
// let mapToJson: StringMap.t(prim) =&gt; string = &lt;fun&gt;;

db11.re

let showJson = true;
// let showJson: bool = true;

let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);
/* let dbGeneric: list(StringMap.t(prim)) =
  [&lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;];
*/
/*
{age: +18, male: false, name: Ada, weight: +98.5}
{age: +25, male: true, name: Ben, weight: +81.5}
{age: +45, alive: true, name: Caz, weight: +70.6}
{age: +10, male: true, name: Dan, weight: +98.5}
{male: false, name: Eve}
*/

db12.re

let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};
// let tryAccessDbGeneric: (StringMap.key, int) =&gt; prim = &lt;fun&gt;;

db13.re

type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};
// type signature = { age: prim, weight: prim, name: prim, male: prim, };

db14.re

let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);
/*
let db: list(signature) =
  [{age: D(18), weight: E(98.5), name: F(&quot;Ada&quot;), male: B(false)},
   {age: D(25), weight: E(81.5), name: F(&quot;Ben&quot;), male: B(true)},
   {age: D(45), weight: E(70.6), name: F(&quot;Caz&quot;), male: A},
   {age: D(10), weight: E(98.5), name: F(&quot;Dan&quot;), male: B(true)},
   {age: A, weight: A, name: F(&quot;Eve&quot;), male: B(false)}];
*/

db15.re

type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
/*
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
*/

db16.re

let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));
/*
let dbCol: signatureColWise =
  {ageList: [D(18), D(25), D(45), D(10), A],
   weightList: [E(98.5), E(81.5), E(70.6), E(98.5), A],
   nameList: [F(&quot;Ada&quot;), F(&quot;Ben&quot;), F(&quot;Caz&quot;), F(&quot;Dan&quot;), F(&quot;Eve&quot;)],
   maleList: [B(false), B(true), A, B(true), B(false)]};
*/

db17.re

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
/* 
type sec =
    G(prim)
  | H(list(sec))
  | I(array(sec))
  | J((string, sec))
  | K({ key: string, value: sec, });
*/

db18.re

exception Unimplemented_type(string);
// exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};
// let secToList: sec =&gt; list(prim) = &lt;fun&gt;;

db19.re

let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};
// let trySecToList: sec =&gt; list(prim) = &lt;fun&gt;;

db2.re

let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
// let toMut: &#x27;a =&gt; mut(&#x27;a) = &lt;fun&gt;;

let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;
// let fromMut: mut(&#x27;a) =&gt; &#x27;a = &lt;fun&gt;;

db20.re

let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}
// let getCounts: list(StringMap.key) =&gt; list((string, int)) = &lt;fun&gt;;

db21.re

let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};
// let getMedian: list(float) =&gt; float = &lt;fun&gt;;

db22.re

let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));
// let getMean: list(float) =&gt; float = &lt;fun&gt;;

db23.re

type stringStats = {
  counts: list((string, int)),
};
// type stringStats = { counts: list((string, int)), };

type floatStats = {
  mean: float,
  median: float,
};
// type floatStats = { mean: float, median: float, };

db24.re

let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};
/*
let listToFloat:
  (list(prim), ~boolAllowed: bool=?, ~intAllowed: bool=?, unit) =&gt; list(float) =
  &lt;fun&gt;;
*/

db25.re

exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};
// let listToString: (list(prim), ~debug: bool=?, unit) =&gt; list(string) = &lt;fun&gt;;

db26.re

let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};
// let getFloatStats: (sec, ~level: int=?, unit) =&gt; floatStats = &lt;fun&gt;;

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}
// let getStringStats: (sec, ~debug: bool=?, unit) =&gt; stringStats = &lt;fun&gt;;

db27.re

let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));
// let primListToSec: list(prim) =&gt; sec = &lt;fun&gt;;

db28.re

let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);
/*
let ages: sec = H([G((D(18))), G((D(25))), G((D(45))), G((D(10))), G(A)]);
let weights: sec =
  H([G((E(98.5))), G((E(81.5))), G((E(70.6))), G((E(98.5))), G(A)]);
let names: sec =
  H([G((F(&quot;Ada&quot;))), G((F(&quot;Ben&quot;))), G((F(&quot;Caz&quot;))), G((F(&quot;Dan&quot;))), G((F(&quot;Eve&quot;)))]);
let males: sec =
  H([G((B(false))), G((B(true))), G(A), G((B(true))), G((B(false)))]);
*/

db29.re

getStringStats(names, ~debug=true, ());
// - : stringStats = {counts: [(&quot;Ada&quot;, 1), (&quot;Ben&quot;, 1), (&quot;Caz&quot;, 1), (&quot;Dan&quot;, 1), (&quot;Eve&quot;, 1)]}

getFloatStats(weights, ~level=1, ());
// - : floatStats = {mean: 87.275, median: 90.}

getStringStats(weights, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;70.6&quot;, 1), (&quot;81.5&quot;, 1), (&quot;98.5&quot;, 2)]}

getFloatStats(ages, ~level=2, ());
// - : floatStats = {mean: 24.5, median: 21.5}

getStringStats(ages, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;10.&quot;, 1), (&quot;18.&quot;, 1), (&quot;25.&quot;, 1), (&quot;45.&quot;, 1)]}

getFloatStats(males, ~level=3, ());
// - : floatStats = {mean: 0.5, median: 0.5}

getStringStats(males, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;0.&quot;, 2), (&quot;1.&quot;, 2)]}

db3.re

let x = ref(0); // Equivalent to let x = toMut(0);
// let x: ref(int) = {contents: 0};

x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);
// - : int = 1

db4.re

type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);
// type prim = A | B(bool) | C(char) | D(int) | E(float) | F(string);

db5.re

let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};
// let change: mut(prim) =&gt; prim = &lt;fun&gt;;

db6.re

let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};
// let toString: mut(prim) =&gt; string = &lt;fun&gt;;

db7.re

let a = toMut(A); toString(a); a.value = change(a); toString(a);
// let a: mut(prim) = {value: A};
// - : string = &quot;empty&quot;
// - : string = &quot;empty&quot;

let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
// let b: mut(prim) = {value: B(false)};
// - : string = &quot;false&quot;
// - : string = &quot;true&quot;

let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
// let c: mut(prim) = {value: C(&#x27;a&#x27;)};
// - : string = &quot;a&quot;
// - : string = &quot;b&quot;

let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
// let d: mut(prim) = {value: D(0)};
// - : string = &quot;0&quot;
// - : string = &quot;+1&quot;

let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
// let e: mut(prim) = {value: E(0.)};
// - : string = &quot;0.&quot;
// - : string = &quot;+1.&quot;

let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);
// let f: mut(prim) = {value: F(&quot;Hello&quot;)};
// - : string = &quot;Hello&quot;
// - : string = &quot;Hello!&quot;

db8.re

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];
/*
let dbRaw: list(array((string, prim))) =
  [[|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(false))|],
   [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)),
     (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)),
     (&quot;alive&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|]];

*/

db9.re

module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});
// module StringMap: { ... };</code></pre><p>Converting our map to a JSON-like string for debug-friendliness:</p><pre><code>db.re

/* HANDLING PRIMITIVE TYPES */

// Mutability in ReasonML is a feature primarily used with records. Here&#x27;s how you define a mutable type that can hold any value:
type mut(&#x27;a) = {
  mutable value: &#x27;a,
};

// In λ-calculus, function types like f: A -&gt; B imply a transformation or proof from A to B. The functions toMut and fromMut serve as bridges between mutable and immutable types, showing they can be interchangeable:
let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;

// Using the standard implementation as a reference, you can see how it translates in practical terms:
let x = ref(0); // Equivalent to let x = toMut(0);
x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);

// ReasonML requires explicit type declarations for union types, unlike TypeScript where you might use &quot;int | null&quot;:
type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);

// Variant types in ReasonML, akin to sum types or dependent types in other languages, are exhaustive and unique, ensuring no overlap between types.

// Handling these types necessitates a switch statement, covering all possible variants for completeness:
let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};

// For pattern matching, especially when not all cases are addressed explicitly, the wildcard &quot;_&quot; can be a fallback. The &quot;when&quot; keyword allows for additional conditions in matches, offering a concise way to handle complex patterns:
let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};

// Testing different cases to demonstrate how these functions work with the defined types:
let a = toMut(A); toString(a); a.value = change(a); toString(a);
let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);

/* DATABASE STORAGE FOR DATA SCIENCE */

// Working with generic types and function handling is one thing, but let&#x27;s step into a scenario where the stakes are higher: being data scientists at a medical center, tasked with deriving basic statistics from patient data. Given a raw database in a text file format, we&#x27;ve managed to extract key information as follows:

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];

// The data&#x27;s format is row-wise with an arbitrary order, which could include duplicates, missing, or extra items. To streamline debugging, we&#x27;re aiming to cast these to string maps.

// Here&#x27;s where the Map.Make functor comes into play, allowing us to generate a StringMap keyed by strings for easier readability and manipulation, akin to handling JSON objects:
module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});

// Converting our map to a JSON-like string for debug-friendliness:
let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};

// Transitioning to a generic database format, our row-wise data gets a transformation. Here, we&#x27;re all about clarity and correctness:
let showJson = true;
let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);

// Accessing the elements becomes straightforward. Missing elements? No biggie, we handle that gracefully:
let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};

// After some exploration and analysis, key insights emerge regarding age, weight, name, and gender. These form the cornerstone of our new database signature:
type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};

// Structuring a strictly-typed database while ensuring all necessary keys are included and defaults are set for missing items:
let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);

// Finally, the database is correctly formatted. Next up, transposing this database to a column-wise format, ready for statistical analysis:
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};

// Successfully transposing our data, we&#x27;re set to dive deep into the analysis, equipped with a database that&#x27;s both comprehensive and accurately structured.
let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));

/* STATISTICS LIBRARY DEVELOPMENT */

// Venturing into building a generic statistics library, we&#x27;re focusing on versatility across different data structures. Whether dealing with Lists or Arrays, the goal is seamless integration and handling.

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
  
// The challenge lies in unpacking these varied structures into a consistent format, ideally a list of primitives, for statistical analysis. Given the evolving nature of our library, not all types are fully supported yet, leading to potential exceptions for unhandled cases.
exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};

// To ensure a smooth user experience, we wrap secToList in a function that gracefully handles exceptions, providing clear feedback rather than abrupt errors.
let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};

// Diving into the core of our library, we aim to offer basic but essential statistical functions, each designed to work with a specific type of data.

// getCounts tackles enumeration, mapping each unique string in a list to its frequency of occurrence, ideal for categorical data analysis.
let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}

// getMedian finds the middle value in a list of floats after sorting, a key measure of central tendency for quantitative data.
let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};

// getMean computes the average from a list of floats, providing a quick snapshot of your data&#x27;s central value.
let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));

// Structuring our output, we define types for summarizing string and float data, encapsulating counts for categorical data and central measures for continuous data.
type stringStats = {
  counts: list((string, int)),
};

type floatStats = {
  mean: float,
  median: float,
};

/* DATA ANALYSIS FRAMEWORK */

// Integrating complex data structures into actionable insights requires a systematic approach. We&#x27;ve established methods to deconstruct complex data into primitive lists and have statistical functions ready. The challenge now is to seamlessly connect these components.

// First, let&#x27;s categorize data types based on their analytical utility:

// - Nominal data, like colors &quot;Blue&quot; and &quot;Yellow&quot;, are distinct without a meaningful order. The mode serves as their central tendency measure.
// - Boolean data, a subset of nominal, consists of binary choices like &quot;Yes&quot; and &quot;No&quot;.
// - Ordinal data, such as ratings from 1 (&quot;Low&quot;) to 5 (&quot;High&quot;), imply order but not the uniformity of scale. Their median reflects central tendency.
// - Numeric data, representing continuous or interval data, can be fully quantified. The mean is used to express their central tendency.

// Recognizing that not all operations apply universally across data types underscores the importance of targeted analytical strategies.

// Transitioning to the implementation phase:

// The `listToFloat` function converts a list of primitives to floats, selectively allowing boolean and integer conversions based on flags:
let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};

// Converting primitives to strings while handling incompatible types by casting to floats, then stringifying, allows for flexible data interpretation:
exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};

// `getFloatStats` and `getStringStats` functions then process these lists into statistical summaries, considering the data level restrictions and debug options respectively:
let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}

// Finally, transforming primitive lists to the expected input format for statistical analysis:
let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));

// Extracting statistics becomes straightforward with prepped data:
let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);

// Now, it&#x27;s just a matter of calling the appropriate statistical function for each data type, with optional debugging for string conversions:
getStringStats(names, ~debug=true, ());
getFloatStats(weights, ~level=1, ());
getStringStats(weights, ~debug=true, ());

getFloatStats(ages, ~level=2, ());
getStringStats(ages, ~debug=true, ());

getFloatStats(males, ~level=3, ());
getStringStats(males, ~debug=true, ());

db1.re

type mut(&#x27;a) = {
  mutable value: &#x27;a,
};
// type mut(&#x27;a) = { mutable value: &#x27;a, };

db10.re

let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};
// let mapToJson: StringMap.t(prim) =&gt; string = &lt;fun&gt;;

db11.re

let showJson = true;
// let showJson: bool = true;

let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);
/* let dbGeneric: list(StringMap.t(prim)) =
  [&lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;];
*/
/*
{age: +18, male: false, name: Ada, weight: +98.5}
{age: +25, male: true, name: Ben, weight: +81.5}
{age: +45, alive: true, name: Caz, weight: +70.6}
{age: +10, male: true, name: Dan, weight: +98.5}
{male: false, name: Eve}
*/

db12.re

let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};
// let tryAccessDbGeneric: (StringMap.key, int) =&gt; prim = &lt;fun&gt;;

db13.re

type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};
// type signature = { age: prim, weight: prim, name: prim, male: prim, };

db14.re

let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);
/*
let db: list(signature) =
  [{age: D(18), weight: E(98.5), name: F(&quot;Ada&quot;), male: B(false)},
   {age: D(25), weight: E(81.5), name: F(&quot;Ben&quot;), male: B(true)},
   {age: D(45), weight: E(70.6), name: F(&quot;Caz&quot;), male: A},
   {age: D(10), weight: E(98.5), name: F(&quot;Dan&quot;), male: B(true)},
   {age: A, weight: A, name: F(&quot;Eve&quot;), male: B(false)}];
*/

db15.re

type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
/*
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
*/

db16.re

let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));
/*
let dbCol: signatureColWise =
  {ageList: [D(18), D(25), D(45), D(10), A],
   weightList: [E(98.5), E(81.5), E(70.6), E(98.5), A],
   nameList: [F(&quot;Ada&quot;), F(&quot;Ben&quot;), F(&quot;Caz&quot;), F(&quot;Dan&quot;), F(&quot;Eve&quot;)],
   maleList: [B(false), B(true), A, B(true), B(false)]};
*/

db17.re

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
/* 
type sec =
    G(prim)
  | H(list(sec))
  | I(array(sec))
  | J((string, sec))
  | K({ key: string, value: sec, });
*/

db18.re

exception Unimplemented_type(string);
// exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};
// let secToList: sec =&gt; list(prim) = &lt;fun&gt;;

db19.re

let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};
// let trySecToList: sec =&gt; list(prim) = &lt;fun&gt;;

db2.re

let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
// let toMut: &#x27;a =&gt; mut(&#x27;a) = &lt;fun&gt;;

let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;
// let fromMut: mut(&#x27;a) =&gt; &#x27;a = &lt;fun&gt;;

db20.re

let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}
// let getCounts: list(StringMap.key) =&gt; list((string, int)) = &lt;fun&gt;;

db21.re

let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};
// let getMedian: list(float) =&gt; float = &lt;fun&gt;;

db22.re

let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));
// let getMean: list(float) =&gt; float = &lt;fun&gt;;

db23.re

type stringStats = {
  counts: list((string, int)),
};
// type stringStats = { counts: list((string, int)), };

type floatStats = {
  mean: float,
  median: float,
};
// type floatStats = { mean: float, median: float, };

db24.re

let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};
/*
let listToFloat:
  (list(prim), ~boolAllowed: bool=?, ~intAllowed: bool=?, unit) =&gt; list(float) =
  &lt;fun&gt;;
*/

db25.re

exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};
// let listToString: (list(prim), ~debug: bool=?, unit) =&gt; list(string) = &lt;fun&gt;;

db26.re

let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};
// let getFloatStats: (sec, ~level: int=?, unit) =&gt; floatStats = &lt;fun&gt;;

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}
// let getStringStats: (sec, ~debug: bool=?, unit) =&gt; stringStats = &lt;fun&gt;;

db27.re

let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));
// let primListToSec: list(prim) =&gt; sec = &lt;fun&gt;;

db28.re

let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);
/*
let ages: sec = H([G((D(18))), G((D(25))), G((D(45))), G((D(10))), G(A)]);
let weights: sec =
  H([G((E(98.5))), G((E(81.5))), G((E(70.6))), G((E(98.5))), G(A)]);
let names: sec =
  H([G((F(&quot;Ada&quot;))), G((F(&quot;Ben&quot;))), G((F(&quot;Caz&quot;))), G((F(&quot;Dan&quot;))), G((F(&quot;Eve&quot;)))]);
let males: sec =
  H([G((B(false))), G((B(true))), G(A), G((B(true))), G((B(false)))]);
*/

db29.re

getStringStats(names, ~debug=true, ());
// - : stringStats = {counts: [(&quot;Ada&quot;, 1), (&quot;Ben&quot;, 1), (&quot;Caz&quot;, 1), (&quot;Dan&quot;, 1), (&quot;Eve&quot;, 1)]}

getFloatStats(weights, ~level=1, ());
// - : floatStats = {mean: 87.275, median: 90.}

getStringStats(weights, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;70.6&quot;, 1), (&quot;81.5&quot;, 1), (&quot;98.5&quot;, 2)]}

getFloatStats(ages, ~level=2, ());
// - : floatStats = {mean: 24.5, median: 21.5}

getStringStats(ages, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;10.&quot;, 1), (&quot;18.&quot;, 1), (&quot;25.&quot;, 1), (&quot;45.&quot;, 1)]}

getFloatStats(males, ~level=3, ());
// - : floatStats = {mean: 0.5, median: 0.5}

getStringStats(males, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;0.&quot;, 2), (&quot;1.&quot;, 2)]}

db3.re

let x = ref(0); // Equivalent to let x = toMut(0);
// let x: ref(int) = {contents: 0};

x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);
// - : int = 1

db4.re

type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);
// type prim = A | B(bool) | C(char) | D(int) | E(float) | F(string);

db5.re

let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};
// let change: mut(prim) =&gt; prim = &lt;fun&gt;;

db6.re

let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};
// let toString: mut(prim) =&gt; string = &lt;fun&gt;;

db7.re

let a = toMut(A); toString(a); a.value = change(a); toString(a);
// let a: mut(prim) = {value: A};
// - : string = &quot;empty&quot;
// - : string = &quot;empty&quot;

let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
// let b: mut(prim) = {value: B(false)};
// - : string = &quot;false&quot;
// - : string = &quot;true&quot;

let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
// let c: mut(prim) = {value: C(&#x27;a&#x27;)};
// - : string = &quot;a&quot;
// - : string = &quot;b&quot;

let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
// let d: mut(prim) = {value: D(0)};
// - : string = &quot;0&quot;
// - : string = &quot;+1&quot;

let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
// let e: mut(prim) = {value: E(0.)};
// - : string = &quot;0.&quot;
// - : string = &quot;+1.&quot;

let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);
// let f: mut(prim) = {value: F(&quot;Hello&quot;)};
// - : string = &quot;Hello&quot;
// - : string = &quot;Hello!&quot;

db8.re

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];
/*
let dbRaw: list(array((string, prim))) =
  [[|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(false))|],
   [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)),
     (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)),
     (&quot;alive&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|]];

*/

db9.re

module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});
// module StringMap: { ... };</code></pre><p>Transitioning to a generic database format, our row-wise data gets a transformation. Here, we’re all about clarity and correctness:</p><pre><code>db.re

/* HANDLING PRIMITIVE TYPES */

// Mutability in ReasonML is a feature primarily used with records. Here&#x27;s how you define a mutable type that can hold any value:
type mut(&#x27;a) = {
  mutable value: &#x27;a,
};

// In λ-calculus, function types like f: A -&gt; B imply a transformation or proof from A to B. The functions toMut and fromMut serve as bridges between mutable and immutable types, showing they can be interchangeable:
let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;

// Using the standard implementation as a reference, you can see how it translates in practical terms:
let x = ref(0); // Equivalent to let x = toMut(0);
x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);

// ReasonML requires explicit type declarations for union types, unlike TypeScript where you might use &quot;int | null&quot;:
type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);

// Variant types in ReasonML, akin to sum types or dependent types in other languages, are exhaustive and unique, ensuring no overlap between types.

// Handling these types necessitates a switch statement, covering all possible variants for completeness:
let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};

// For pattern matching, especially when not all cases are addressed explicitly, the wildcard &quot;_&quot; can be a fallback. The &quot;when&quot; keyword allows for additional conditions in matches, offering a concise way to handle complex patterns:
let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};

// Testing different cases to demonstrate how these functions work with the defined types:
let a = toMut(A); toString(a); a.value = change(a); toString(a);
let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);

/* DATABASE STORAGE FOR DATA SCIENCE */

// Working with generic types and function handling is one thing, but let&#x27;s step into a scenario where the stakes are higher: being data scientists at a medical center, tasked with deriving basic statistics from patient data. Given a raw database in a text file format, we&#x27;ve managed to extract key information as follows:

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];

// The data&#x27;s format is row-wise with an arbitrary order, which could include duplicates, missing, or extra items. To streamline debugging, we&#x27;re aiming to cast these to string maps.

// Here&#x27;s where the Map.Make functor comes into play, allowing us to generate a StringMap keyed by strings for easier readability and manipulation, akin to handling JSON objects:
module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});

// Converting our map to a JSON-like string for debug-friendliness:
let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};

// Transitioning to a generic database format, our row-wise data gets a transformation. Here, we&#x27;re all about clarity and correctness:
let showJson = true;
let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);

// Accessing the elements becomes straightforward. Missing elements? No biggie, we handle that gracefully:
let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};

// After some exploration and analysis, key insights emerge regarding age, weight, name, and gender. These form the cornerstone of our new database signature:
type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};

// Structuring a strictly-typed database while ensuring all necessary keys are included and defaults are set for missing items:
let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);

// Finally, the database is correctly formatted. Next up, transposing this database to a column-wise format, ready for statistical analysis:
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};

// Successfully transposing our data, we&#x27;re set to dive deep into the analysis, equipped with a database that&#x27;s both comprehensive and accurately structured.
let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));

/* STATISTICS LIBRARY DEVELOPMENT */

// Venturing into building a generic statistics library, we&#x27;re focusing on versatility across different data structures. Whether dealing with Lists or Arrays, the goal is seamless integration and handling.

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
  
// The challenge lies in unpacking these varied structures into a consistent format, ideally a list of primitives, for statistical analysis. Given the evolving nature of our library, not all types are fully supported yet, leading to potential exceptions for unhandled cases.
exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};

// To ensure a smooth user experience, we wrap secToList in a function that gracefully handles exceptions, providing clear feedback rather than abrupt errors.
let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};

// Diving into the core of our library, we aim to offer basic but essential statistical functions, each designed to work with a specific type of data.

// getCounts tackles enumeration, mapping each unique string in a list to its frequency of occurrence, ideal for categorical data analysis.
let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}

// getMedian finds the middle value in a list of floats after sorting, a key measure of central tendency for quantitative data.
let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};

// getMean computes the average from a list of floats, providing a quick snapshot of your data&#x27;s central value.
let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));

// Structuring our output, we define types for summarizing string and float data, encapsulating counts for categorical data and central measures for continuous data.
type stringStats = {
  counts: list((string, int)),
};

type floatStats = {
  mean: float,
  median: float,
};

/* DATA ANALYSIS FRAMEWORK */

// Integrating complex data structures into actionable insights requires a systematic approach. We&#x27;ve established methods to deconstruct complex data into primitive lists and have statistical functions ready. The challenge now is to seamlessly connect these components.

// First, let&#x27;s categorize data types based on their analytical utility:

// - Nominal data, like colors &quot;Blue&quot; and &quot;Yellow&quot;, are distinct without a meaningful order. The mode serves as their central tendency measure.
// - Boolean data, a subset of nominal, consists of binary choices like &quot;Yes&quot; and &quot;No&quot;.
// - Ordinal data, such as ratings from 1 (&quot;Low&quot;) to 5 (&quot;High&quot;), imply order but not the uniformity of scale. Their median reflects central tendency.
// - Numeric data, representing continuous or interval data, can be fully quantified. The mean is used to express their central tendency.

// Recognizing that not all operations apply universally across data types underscores the importance of targeted analytical strategies.

// Transitioning to the implementation phase:

// The `listToFloat` function converts a list of primitives to floats, selectively allowing boolean and integer conversions based on flags:
let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};

// Converting primitives to strings while handling incompatible types by casting to floats, then stringifying, allows for flexible data interpretation:
exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};

// `getFloatStats` and `getStringStats` functions then process these lists into statistical summaries, considering the data level restrictions and debug options respectively:
let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}

// Finally, transforming primitive lists to the expected input format for statistical analysis:
let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));

// Extracting statistics becomes straightforward with prepped data:
let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);

// Now, it&#x27;s just a matter of calling the appropriate statistical function for each data type, with optional debugging for string conversions:
getStringStats(names, ~debug=true, ());
getFloatStats(weights, ~level=1, ());
getStringStats(weights, ~debug=true, ());

getFloatStats(ages, ~level=2, ());
getStringStats(ages, ~debug=true, ());

getFloatStats(males, ~level=3, ());
getStringStats(males, ~debug=true, ());

db1.re

type mut(&#x27;a) = {
  mutable value: &#x27;a,
};
// type mut(&#x27;a) = { mutable value: &#x27;a, };

db10.re

let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};
// let mapToJson: StringMap.t(prim) =&gt; string = &lt;fun&gt;;

db11.re

let showJson = true;
// let showJson: bool = true;

let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);
/* let dbGeneric: list(StringMap.t(prim)) =
  [&lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;];
*/
/*
{age: +18, male: false, name: Ada, weight: +98.5}
{age: +25, male: true, name: Ben, weight: +81.5}
{age: +45, alive: true, name: Caz, weight: +70.6}
{age: +10, male: true, name: Dan, weight: +98.5}
{male: false, name: Eve}
*/

db12.re

let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};
// let tryAccessDbGeneric: (StringMap.key, int) =&gt; prim = &lt;fun&gt;;

db13.re

type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};
// type signature = { age: prim, weight: prim, name: prim, male: prim, };

db14.re

let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);
/*
let db: list(signature) =
  [{age: D(18), weight: E(98.5), name: F(&quot;Ada&quot;), male: B(false)},
   {age: D(25), weight: E(81.5), name: F(&quot;Ben&quot;), male: B(true)},
   {age: D(45), weight: E(70.6), name: F(&quot;Caz&quot;), male: A},
   {age: D(10), weight: E(98.5), name: F(&quot;Dan&quot;), male: B(true)},
   {age: A, weight: A, name: F(&quot;Eve&quot;), male: B(false)}];
*/

db15.re

type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
/*
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
*/

db16.re

let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));
/*
let dbCol: signatureColWise =
  {ageList: [D(18), D(25), D(45), D(10), A],
   weightList: [E(98.5), E(81.5), E(70.6), E(98.5), A],
   nameList: [F(&quot;Ada&quot;), F(&quot;Ben&quot;), F(&quot;Caz&quot;), F(&quot;Dan&quot;), F(&quot;Eve&quot;)],
   maleList: [B(false), B(true), A, B(true), B(false)]};
*/

db17.re

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
/* 
type sec =
    G(prim)
  | H(list(sec))
  | I(array(sec))
  | J((string, sec))
  | K({ key: string, value: sec, });
*/

db18.re

exception Unimplemented_type(string);
// exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};
// let secToList: sec =&gt; list(prim) = &lt;fun&gt;;

db19.re

let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};
// let trySecToList: sec =&gt; list(prim) = &lt;fun&gt;;

db2.re

let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
// let toMut: &#x27;a =&gt; mut(&#x27;a) = &lt;fun&gt;;

let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;
// let fromMut: mut(&#x27;a) =&gt; &#x27;a = &lt;fun&gt;;

db20.re

let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}
// let getCounts: list(StringMap.key) =&gt; list((string, int)) = &lt;fun&gt;;

db21.re

let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};
// let getMedian: list(float) =&gt; float = &lt;fun&gt;;

db22.re

let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));
// let getMean: list(float) =&gt; float = &lt;fun&gt;;

db23.re

type stringStats = {
  counts: list((string, int)),
};
// type stringStats = { counts: list((string, int)), };

type floatStats = {
  mean: float,
  median: float,
};
// type floatStats = { mean: float, median: float, };

db24.re

let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};
/*
let listToFloat:
  (list(prim), ~boolAllowed: bool=?, ~intAllowed: bool=?, unit) =&gt; list(float) =
  &lt;fun&gt;;
*/

db25.re

exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};
// let listToString: (list(prim), ~debug: bool=?, unit) =&gt; list(string) = &lt;fun&gt;;

db26.re

let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};
// let getFloatStats: (sec, ~level: int=?, unit) =&gt; floatStats = &lt;fun&gt;;

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}
// let getStringStats: (sec, ~debug: bool=?, unit) =&gt; stringStats = &lt;fun&gt;;

db27.re

let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));
// let primListToSec: list(prim) =&gt; sec = &lt;fun&gt;;

db28.re

let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);
/*
let ages: sec = H([G((D(18))), G((D(25))), G((D(45))), G((D(10))), G(A)]);
let weights: sec =
  H([G((E(98.5))), G((E(81.5))), G((E(70.6))), G((E(98.5))), G(A)]);
let names: sec =
  H([G((F(&quot;Ada&quot;))), G((F(&quot;Ben&quot;))), G((F(&quot;Caz&quot;))), G((F(&quot;Dan&quot;))), G((F(&quot;Eve&quot;)))]);
let males: sec =
  H([G((B(false))), G((B(true))), G(A), G((B(true))), G((B(false)))]);
*/

db29.re

getStringStats(names, ~debug=true, ());
// - : stringStats = {counts: [(&quot;Ada&quot;, 1), (&quot;Ben&quot;, 1), (&quot;Caz&quot;, 1), (&quot;Dan&quot;, 1), (&quot;Eve&quot;, 1)]}

getFloatStats(weights, ~level=1, ());
// - : floatStats = {mean: 87.275, median: 90.}

getStringStats(weights, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;70.6&quot;, 1), (&quot;81.5&quot;, 1), (&quot;98.5&quot;, 2)]}

getFloatStats(ages, ~level=2, ());
// - : floatStats = {mean: 24.5, median: 21.5}

getStringStats(ages, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;10.&quot;, 1), (&quot;18.&quot;, 1), (&quot;25.&quot;, 1), (&quot;45.&quot;, 1)]}

getFloatStats(males, ~level=3, ());
// - : floatStats = {mean: 0.5, median: 0.5}

getStringStats(males, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;0.&quot;, 2), (&quot;1.&quot;, 2)]}

db3.re

let x = ref(0); // Equivalent to let x = toMut(0);
// let x: ref(int) = {contents: 0};

x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);
// - : int = 1

db4.re

type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);
// type prim = A | B(bool) | C(char) | D(int) | E(float) | F(string);

db5.re

let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};
// let change: mut(prim) =&gt; prim = &lt;fun&gt;;

db6.re

let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};
// let toString: mut(prim) =&gt; string = &lt;fun&gt;;

db7.re

let a = toMut(A); toString(a); a.value = change(a); toString(a);
// let a: mut(prim) = {value: A};
// - : string = &quot;empty&quot;
// - : string = &quot;empty&quot;

let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
// let b: mut(prim) = {value: B(false)};
// - : string = &quot;false&quot;
// - : string = &quot;true&quot;

let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
// let c: mut(prim) = {value: C(&#x27;a&#x27;)};
// - : string = &quot;a&quot;
// - : string = &quot;b&quot;

let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
// let d: mut(prim) = {value: D(0)};
// - : string = &quot;0&quot;
// - : string = &quot;+1&quot;

let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
// let e: mut(prim) = {value: E(0.)};
// - : string = &quot;0.&quot;
// - : string = &quot;+1.&quot;

let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);
// let f: mut(prim) = {value: F(&quot;Hello&quot;)};
// - : string = &quot;Hello&quot;
// - : string = &quot;Hello!&quot;

db8.re

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];
/*
let dbRaw: list(array((string, prim))) =
  [[|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(false))|],
   [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)),
     (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)),
     (&quot;alive&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|]];

*/

db9.re

module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});
// module StringMap: { ... };</code></pre><p>Accessing the elements becomes straightforward. Missing elements? No biggie, we handle that gracefully:</p><pre><code>db.re

/* HANDLING PRIMITIVE TYPES */

// Mutability in ReasonML is a feature primarily used with records. Here&#x27;s how you define a mutable type that can hold any value:
type mut(&#x27;a) = {
  mutable value: &#x27;a,
};

// In λ-calculus, function types like f: A -&gt; B imply a transformation or proof from A to B. The functions toMut and fromMut serve as bridges between mutable and immutable types, showing they can be interchangeable:
let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;

// Using the standard implementation as a reference, you can see how it translates in practical terms:
let x = ref(0); // Equivalent to let x = toMut(0);
x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);

// ReasonML requires explicit type declarations for union types, unlike TypeScript where you might use &quot;int | null&quot;:
type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);

// Variant types in ReasonML, akin to sum types or dependent types in other languages, are exhaustive and unique, ensuring no overlap between types.

// Handling these types necessitates a switch statement, covering all possible variants for completeness:
let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};

// For pattern matching, especially when not all cases are addressed explicitly, the wildcard &quot;_&quot; can be a fallback. The &quot;when&quot; keyword allows for additional conditions in matches, offering a concise way to handle complex patterns:
let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};

// Testing different cases to demonstrate how these functions work with the defined types:
let a = toMut(A); toString(a); a.value = change(a); toString(a);
let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);

/* DATABASE STORAGE FOR DATA SCIENCE */

// Working with generic types and function handling is one thing, but let&#x27;s step into a scenario where the stakes are higher: being data scientists at a medical center, tasked with deriving basic statistics from patient data. Given a raw database in a text file format, we&#x27;ve managed to extract key information as follows:

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];

// The data&#x27;s format is row-wise with an arbitrary order, which could include duplicates, missing, or extra items. To streamline debugging, we&#x27;re aiming to cast these to string maps.

// Here&#x27;s where the Map.Make functor comes into play, allowing us to generate a StringMap keyed by strings for easier readability and manipulation, akin to handling JSON objects:
module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});

// Converting our map to a JSON-like string for debug-friendliness:
let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};

// Transitioning to a generic database format, our row-wise data gets a transformation. Here, we&#x27;re all about clarity and correctness:
let showJson = true;
let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);

// Accessing the elements becomes straightforward. Missing elements? No biggie, we handle that gracefully:
let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};

// After some exploration and analysis, key insights emerge regarding age, weight, name, and gender. These form the cornerstone of our new database signature:
type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};

// Structuring a strictly-typed database while ensuring all necessary keys are included and defaults are set for missing items:
let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);

// Finally, the database is correctly formatted. Next up, transposing this database to a column-wise format, ready for statistical analysis:
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};

// Successfully transposing our data, we&#x27;re set to dive deep into the analysis, equipped with a database that&#x27;s both comprehensive and accurately structured.
let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));

/* STATISTICS LIBRARY DEVELOPMENT */

// Venturing into building a generic statistics library, we&#x27;re focusing on versatility across different data structures. Whether dealing with Lists or Arrays, the goal is seamless integration and handling.

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
  
// The challenge lies in unpacking these varied structures into a consistent format, ideally a list of primitives, for statistical analysis. Given the evolving nature of our library, not all types are fully supported yet, leading to potential exceptions for unhandled cases.
exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};

// To ensure a smooth user experience, we wrap secToList in a function that gracefully handles exceptions, providing clear feedback rather than abrupt errors.
let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};

// Diving into the core of our library, we aim to offer basic but essential statistical functions, each designed to work with a specific type of data.

// getCounts tackles enumeration, mapping each unique string in a list to its frequency of occurrence, ideal for categorical data analysis.
let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}

// getMedian finds the middle value in a list of floats after sorting, a key measure of central tendency for quantitative data.
let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};

// getMean computes the average from a list of floats, providing a quick snapshot of your data&#x27;s central value.
let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));

// Structuring our output, we define types for summarizing string and float data, encapsulating counts for categorical data and central measures for continuous data.
type stringStats = {
  counts: list((string, int)),
};

type floatStats = {
  mean: float,
  median: float,
};

/* DATA ANALYSIS FRAMEWORK */

// Integrating complex data structures into actionable insights requires a systematic approach. We&#x27;ve established methods to deconstruct complex data into primitive lists and have statistical functions ready. The challenge now is to seamlessly connect these components.

// First, let&#x27;s categorize data types based on their analytical utility:

// - Nominal data, like colors &quot;Blue&quot; and &quot;Yellow&quot;, are distinct without a meaningful order. The mode serves as their central tendency measure.
// - Boolean data, a subset of nominal, consists of binary choices like &quot;Yes&quot; and &quot;No&quot;.
// - Ordinal data, such as ratings from 1 (&quot;Low&quot;) to 5 (&quot;High&quot;), imply order but not the uniformity of scale. Their median reflects central tendency.
// - Numeric data, representing continuous or interval data, can be fully quantified. The mean is used to express their central tendency.

// Recognizing that not all operations apply universally across data types underscores the importance of targeted analytical strategies.

// Transitioning to the implementation phase:

// The `listToFloat` function converts a list of primitives to floats, selectively allowing boolean and integer conversions based on flags:
let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};

// Converting primitives to strings while handling incompatible types by casting to floats, then stringifying, allows for flexible data interpretation:
exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};

// `getFloatStats` and `getStringStats` functions then process these lists into statistical summaries, considering the data level restrictions and debug options respectively:
let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}

// Finally, transforming primitive lists to the expected input format for statistical analysis:
let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));

// Extracting statistics becomes straightforward with prepped data:
let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);

// Now, it&#x27;s just a matter of calling the appropriate statistical function for each data type, with optional debugging for string conversions:
getStringStats(names, ~debug=true, ());
getFloatStats(weights, ~level=1, ());
getStringStats(weights, ~debug=true, ());

getFloatStats(ages, ~level=2, ());
getStringStats(ages, ~debug=true, ());

getFloatStats(males, ~level=3, ());
getStringStats(males, ~debug=true, ());

db1.re

type mut(&#x27;a) = {
  mutable value: &#x27;a,
};
// type mut(&#x27;a) = { mutable value: &#x27;a, };

db10.re

let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};
// let mapToJson: StringMap.t(prim) =&gt; string = &lt;fun&gt;;

db11.re

let showJson = true;
// let showJson: bool = true;

let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);
/* let dbGeneric: list(StringMap.t(prim)) =
  [&lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;];
*/
/*
{age: +18, male: false, name: Ada, weight: +98.5}
{age: +25, male: true, name: Ben, weight: +81.5}
{age: +45, alive: true, name: Caz, weight: +70.6}
{age: +10, male: true, name: Dan, weight: +98.5}
{male: false, name: Eve}
*/

db12.re

let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};
// let tryAccessDbGeneric: (StringMap.key, int) =&gt; prim = &lt;fun&gt;;

db13.re

type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};
// type signature = { age: prim, weight: prim, name: prim, male: prim, };

db14.re

let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);
/*
let db: list(signature) =
  [{age: D(18), weight: E(98.5), name: F(&quot;Ada&quot;), male: B(false)},
   {age: D(25), weight: E(81.5), name: F(&quot;Ben&quot;), male: B(true)},
   {age: D(45), weight: E(70.6), name: F(&quot;Caz&quot;), male: A},
   {age: D(10), weight: E(98.5), name: F(&quot;Dan&quot;), male: B(true)},
   {age: A, weight: A, name: F(&quot;Eve&quot;), male: B(false)}];
*/

db15.re

type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
/*
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
*/

db16.re

let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));
/*
let dbCol: signatureColWise =
  {ageList: [D(18), D(25), D(45), D(10), A],
   weightList: [E(98.5), E(81.5), E(70.6), E(98.5), A],
   nameList: [F(&quot;Ada&quot;), F(&quot;Ben&quot;), F(&quot;Caz&quot;), F(&quot;Dan&quot;), F(&quot;Eve&quot;)],
   maleList: [B(false), B(true), A, B(true), B(false)]};
*/

db17.re

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
/* 
type sec =
    G(prim)
  | H(list(sec))
  | I(array(sec))
  | J((string, sec))
  | K({ key: string, value: sec, });
*/

db18.re

exception Unimplemented_type(string);
// exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};
// let secToList: sec =&gt; list(prim) = &lt;fun&gt;;

db19.re

let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};
// let trySecToList: sec =&gt; list(prim) = &lt;fun&gt;;

db2.re

let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
// let toMut: &#x27;a =&gt; mut(&#x27;a) = &lt;fun&gt;;

let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;
// let fromMut: mut(&#x27;a) =&gt; &#x27;a = &lt;fun&gt;;

db20.re

let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}
// let getCounts: list(StringMap.key) =&gt; list((string, int)) = &lt;fun&gt;;

db21.re

let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};
// let getMedian: list(float) =&gt; float = &lt;fun&gt;;

db22.re

let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));
// let getMean: list(float) =&gt; float = &lt;fun&gt;;

db23.re

type stringStats = {
  counts: list((string, int)),
};
// type stringStats = { counts: list((string, int)), };

type floatStats = {
  mean: float,
  median: float,
};
// type floatStats = { mean: float, median: float, };

db24.re

let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};
/*
let listToFloat:
  (list(prim), ~boolAllowed: bool=?, ~intAllowed: bool=?, unit) =&gt; list(float) =
  &lt;fun&gt;;
*/

db25.re

exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};
// let listToString: (list(prim), ~debug: bool=?, unit) =&gt; list(string) = &lt;fun&gt;;

db26.re

let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};
// let getFloatStats: (sec, ~level: int=?, unit) =&gt; floatStats = &lt;fun&gt;;

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}
// let getStringStats: (sec, ~debug: bool=?, unit) =&gt; stringStats = &lt;fun&gt;;

db27.re

let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));
// let primListToSec: list(prim) =&gt; sec = &lt;fun&gt;;

db28.re

let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);
/*
let ages: sec = H([G((D(18))), G((D(25))), G((D(45))), G((D(10))), G(A)]);
let weights: sec =
  H([G((E(98.5))), G((E(81.5))), G((E(70.6))), G((E(98.5))), G(A)]);
let names: sec =
  H([G((F(&quot;Ada&quot;))), G((F(&quot;Ben&quot;))), G((F(&quot;Caz&quot;))), G((F(&quot;Dan&quot;))), G((F(&quot;Eve&quot;)))]);
let males: sec =
  H([G((B(false))), G((B(true))), G(A), G((B(true))), G((B(false)))]);
*/

db29.re

getStringStats(names, ~debug=true, ());
// - : stringStats = {counts: [(&quot;Ada&quot;, 1), (&quot;Ben&quot;, 1), (&quot;Caz&quot;, 1), (&quot;Dan&quot;, 1), (&quot;Eve&quot;, 1)]}

getFloatStats(weights, ~level=1, ());
// - : floatStats = {mean: 87.275, median: 90.}

getStringStats(weights, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;70.6&quot;, 1), (&quot;81.5&quot;, 1), (&quot;98.5&quot;, 2)]}

getFloatStats(ages, ~level=2, ());
// - : floatStats = {mean: 24.5, median: 21.5}

getStringStats(ages, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;10.&quot;, 1), (&quot;18.&quot;, 1), (&quot;25.&quot;, 1), (&quot;45.&quot;, 1)]}

getFloatStats(males, ~level=3, ());
// - : floatStats = {mean: 0.5, median: 0.5}

getStringStats(males, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;0.&quot;, 2), (&quot;1.&quot;, 2)]}

db3.re

let x = ref(0); // Equivalent to let x = toMut(0);
// let x: ref(int) = {contents: 0};

x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);
// - : int = 1

db4.re

type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);
// type prim = A | B(bool) | C(char) | D(int) | E(float) | F(string);

db5.re

let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};
// let change: mut(prim) =&gt; prim = &lt;fun&gt;;

db6.re

let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};
// let toString: mut(prim) =&gt; string = &lt;fun&gt;;

db7.re

let a = toMut(A); toString(a); a.value = change(a); toString(a);
// let a: mut(prim) = {value: A};
// - : string = &quot;empty&quot;
// - : string = &quot;empty&quot;

let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
// let b: mut(prim) = {value: B(false)};
// - : string = &quot;false&quot;
// - : string = &quot;true&quot;

let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
// let c: mut(prim) = {value: C(&#x27;a&#x27;)};
// - : string = &quot;a&quot;
// - : string = &quot;b&quot;

let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
// let d: mut(prim) = {value: D(0)};
// - : string = &quot;0&quot;
// - : string = &quot;+1&quot;

let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
// let e: mut(prim) = {value: E(0.)};
// - : string = &quot;0.&quot;
// - : string = &quot;+1.&quot;

let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);
// let f: mut(prim) = {value: F(&quot;Hello&quot;)};
// - : string = &quot;Hello&quot;
// - : string = &quot;Hello!&quot;

db8.re

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];
/*
let dbRaw: list(array((string, prim))) =
  [[|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(false))|],
   [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)),
     (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)),
     (&quot;alive&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|]];

*/

db9.re

module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});
// module StringMap: { ... };</code></pre><p>After some exploration and analysis, key insights emerge regarding age, weight, name, and gender. These form the cornerstone of our new database signature:</p><pre><code>db.re

/* HANDLING PRIMITIVE TYPES */

// Mutability in ReasonML is a feature primarily used with records. Here&#x27;s how you define a mutable type that can hold any value:
type mut(&#x27;a) = {
  mutable value: &#x27;a,
};

// In λ-calculus, function types like f: A -&gt; B imply a transformation or proof from A to B. The functions toMut and fromMut serve as bridges between mutable and immutable types, showing they can be interchangeable:
let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;

// Using the standard implementation as a reference, you can see how it translates in practical terms:
let x = ref(0); // Equivalent to let x = toMut(0);
x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);

// ReasonML requires explicit type declarations for union types, unlike TypeScript where you might use &quot;int | null&quot;:
type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);

// Variant types in ReasonML, akin to sum types or dependent types in other languages, are exhaustive and unique, ensuring no overlap between types.

// Handling these types necessitates a switch statement, covering all possible variants for completeness:
let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};

// For pattern matching, especially when not all cases are addressed explicitly, the wildcard &quot;_&quot; can be a fallback. The &quot;when&quot; keyword allows for additional conditions in matches, offering a concise way to handle complex patterns:
let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};

// Testing different cases to demonstrate how these functions work with the defined types:
let a = toMut(A); toString(a); a.value = change(a); toString(a);
let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);

/* DATABASE STORAGE FOR DATA SCIENCE */

// Working with generic types and function handling is one thing, but let&#x27;s step into a scenario where the stakes are higher: being data scientists at a medical center, tasked with deriving basic statistics from patient data. Given a raw database in a text file format, we&#x27;ve managed to extract key information as follows:

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];

// The data&#x27;s format is row-wise with an arbitrary order, which could include duplicates, missing, or extra items. To streamline debugging, we&#x27;re aiming to cast these to string maps.

// Here&#x27;s where the Map.Make functor comes into play, allowing us to generate a StringMap keyed by strings for easier readability and manipulation, akin to handling JSON objects:
module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});

// Converting our map to a JSON-like string for debug-friendliness:
let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};

// Transitioning to a generic database format, our row-wise data gets a transformation. Here, we&#x27;re all about clarity and correctness:
let showJson = true;
let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);

// Accessing the elements becomes straightforward. Missing elements? No biggie, we handle that gracefully:
let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};

// After some exploration and analysis, key insights emerge regarding age, weight, name, and gender. These form the cornerstone of our new database signature:
type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};

// Structuring a strictly-typed database while ensuring all necessary keys are included and defaults are set for missing items:
let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);

// Finally, the database is correctly formatted. Next up, transposing this database to a column-wise format, ready for statistical analysis:
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};

// Successfully transposing our data, we&#x27;re set to dive deep into the analysis, equipped with a database that&#x27;s both comprehensive and accurately structured.
let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));

/* STATISTICS LIBRARY DEVELOPMENT */

// Venturing into building a generic statistics library, we&#x27;re focusing on versatility across different data structures. Whether dealing with Lists or Arrays, the goal is seamless integration and handling.

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
  
// The challenge lies in unpacking these varied structures into a consistent format, ideally a list of primitives, for statistical analysis. Given the evolving nature of our library, not all types are fully supported yet, leading to potential exceptions for unhandled cases.
exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};

// To ensure a smooth user experience, we wrap secToList in a function that gracefully handles exceptions, providing clear feedback rather than abrupt errors.
let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};

// Diving into the core of our library, we aim to offer basic but essential statistical functions, each designed to work with a specific type of data.

// getCounts tackles enumeration, mapping each unique string in a list to its frequency of occurrence, ideal for categorical data analysis.
let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}

// getMedian finds the middle value in a list of floats after sorting, a key measure of central tendency for quantitative data.
let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};

// getMean computes the average from a list of floats, providing a quick snapshot of your data&#x27;s central value.
let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));

// Structuring our output, we define types for summarizing string and float data, encapsulating counts for categorical data and central measures for continuous data.
type stringStats = {
  counts: list((string, int)),
};

type floatStats = {
  mean: float,
  median: float,
};

/* DATA ANALYSIS FRAMEWORK */

// Integrating complex data structures into actionable insights requires a systematic approach. We&#x27;ve established methods to deconstruct complex data into primitive lists and have statistical functions ready. The challenge now is to seamlessly connect these components.

// First, let&#x27;s categorize data types based on their analytical utility:

// - Nominal data, like colors &quot;Blue&quot; and &quot;Yellow&quot;, are distinct without a meaningful order. The mode serves as their central tendency measure.
// - Boolean data, a subset of nominal, consists of binary choices like &quot;Yes&quot; and &quot;No&quot;.
// - Ordinal data, such as ratings from 1 (&quot;Low&quot;) to 5 (&quot;High&quot;), imply order but not the uniformity of scale. Their median reflects central tendency.
// - Numeric data, representing continuous or interval data, can be fully quantified. The mean is used to express their central tendency.

// Recognizing that not all operations apply universally across data types underscores the importance of targeted analytical strategies.

// Transitioning to the implementation phase:

// The `listToFloat` function converts a list of primitives to floats, selectively allowing boolean and integer conversions based on flags:
let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};

// Converting primitives to strings while handling incompatible types by casting to floats, then stringifying, allows for flexible data interpretation:
exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};

// `getFloatStats` and `getStringStats` functions then process these lists into statistical summaries, considering the data level restrictions and debug options respectively:
let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}

// Finally, transforming primitive lists to the expected input format for statistical analysis:
let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));

// Extracting statistics becomes straightforward with prepped data:
let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);

// Now, it&#x27;s just a matter of calling the appropriate statistical function for each data type, with optional debugging for string conversions:
getStringStats(names, ~debug=true, ());
getFloatStats(weights, ~level=1, ());
getStringStats(weights, ~debug=true, ());

getFloatStats(ages, ~level=2, ());
getStringStats(ages, ~debug=true, ());

getFloatStats(males, ~level=3, ());
getStringStats(males, ~debug=true, ());

db1.re

type mut(&#x27;a) = {
  mutable value: &#x27;a,
};
// type mut(&#x27;a) = { mutable value: &#x27;a, };

db10.re

let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};
// let mapToJson: StringMap.t(prim) =&gt; string = &lt;fun&gt;;

db11.re

let showJson = true;
// let showJson: bool = true;

let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);
/* let dbGeneric: list(StringMap.t(prim)) =
  [&lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;];
*/
/*
{age: +18, male: false, name: Ada, weight: +98.5}
{age: +25, male: true, name: Ben, weight: +81.5}
{age: +45, alive: true, name: Caz, weight: +70.6}
{age: +10, male: true, name: Dan, weight: +98.5}
{male: false, name: Eve}
*/

db12.re

let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};
// let tryAccessDbGeneric: (StringMap.key, int) =&gt; prim = &lt;fun&gt;;

db13.re

type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};
// type signature = { age: prim, weight: prim, name: prim, male: prim, };

db14.re

let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);
/*
let db: list(signature) =
  [{age: D(18), weight: E(98.5), name: F(&quot;Ada&quot;), male: B(false)},
   {age: D(25), weight: E(81.5), name: F(&quot;Ben&quot;), male: B(true)},
   {age: D(45), weight: E(70.6), name: F(&quot;Caz&quot;), male: A},
   {age: D(10), weight: E(98.5), name: F(&quot;Dan&quot;), male: B(true)},
   {age: A, weight: A, name: F(&quot;Eve&quot;), male: B(false)}];
*/

db15.re

type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
/*
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
*/

db16.re

let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));
/*
let dbCol: signatureColWise =
  {ageList: [D(18), D(25), D(45), D(10), A],
   weightList: [E(98.5), E(81.5), E(70.6), E(98.5), A],
   nameList: [F(&quot;Ada&quot;), F(&quot;Ben&quot;), F(&quot;Caz&quot;), F(&quot;Dan&quot;), F(&quot;Eve&quot;)],
   maleList: [B(false), B(true), A, B(true), B(false)]};
*/

db17.re

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
/* 
type sec =
    G(prim)
  | H(list(sec))
  | I(array(sec))
  | J((string, sec))
  | K({ key: string, value: sec, });
*/

db18.re

exception Unimplemented_type(string);
// exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};
// let secToList: sec =&gt; list(prim) = &lt;fun&gt;;

db19.re

let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};
// let trySecToList: sec =&gt; list(prim) = &lt;fun&gt;;

db2.re

let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
// let toMut: &#x27;a =&gt; mut(&#x27;a) = &lt;fun&gt;;

let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;
// let fromMut: mut(&#x27;a) =&gt; &#x27;a = &lt;fun&gt;;

db20.re

let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}
// let getCounts: list(StringMap.key) =&gt; list((string, int)) = &lt;fun&gt;;

db21.re

let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};
// let getMedian: list(float) =&gt; float = &lt;fun&gt;;

db22.re

let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));
// let getMean: list(float) =&gt; float = &lt;fun&gt;;

db23.re

type stringStats = {
  counts: list((string, int)),
};
// type stringStats = { counts: list((string, int)), };

type floatStats = {
  mean: float,
  median: float,
};
// type floatStats = { mean: float, median: float, };

db24.re

let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};
/*
let listToFloat:
  (list(prim), ~boolAllowed: bool=?, ~intAllowed: bool=?, unit) =&gt; list(float) =
  &lt;fun&gt;;
*/

db25.re

exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};
// let listToString: (list(prim), ~debug: bool=?, unit) =&gt; list(string) = &lt;fun&gt;;

db26.re

let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};
// let getFloatStats: (sec, ~level: int=?, unit) =&gt; floatStats = &lt;fun&gt;;

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}
// let getStringStats: (sec, ~debug: bool=?, unit) =&gt; stringStats = &lt;fun&gt;;

db27.re

let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));
// let primListToSec: list(prim) =&gt; sec = &lt;fun&gt;;

db28.re

let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);
/*
let ages: sec = H([G((D(18))), G((D(25))), G((D(45))), G((D(10))), G(A)]);
let weights: sec =
  H([G((E(98.5))), G((E(81.5))), G((E(70.6))), G((E(98.5))), G(A)]);
let names: sec =
  H([G((F(&quot;Ada&quot;))), G((F(&quot;Ben&quot;))), G((F(&quot;Caz&quot;))), G((F(&quot;Dan&quot;))), G((F(&quot;Eve&quot;)))]);
let males: sec =
  H([G((B(false))), G((B(true))), G(A), G((B(true))), G((B(false)))]);
*/

db29.re

getStringStats(names, ~debug=true, ());
// - : stringStats = {counts: [(&quot;Ada&quot;, 1), (&quot;Ben&quot;, 1), (&quot;Caz&quot;, 1), (&quot;Dan&quot;, 1), (&quot;Eve&quot;, 1)]}

getFloatStats(weights, ~level=1, ());
// - : floatStats = {mean: 87.275, median: 90.}

getStringStats(weights, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;70.6&quot;, 1), (&quot;81.5&quot;, 1), (&quot;98.5&quot;, 2)]}

getFloatStats(ages, ~level=2, ());
// - : floatStats = {mean: 24.5, median: 21.5}

getStringStats(ages, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;10.&quot;, 1), (&quot;18.&quot;, 1), (&quot;25.&quot;, 1), (&quot;45.&quot;, 1)]}

getFloatStats(males, ~level=3, ());
// - : floatStats = {mean: 0.5, median: 0.5}

getStringStats(males, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;0.&quot;, 2), (&quot;1.&quot;, 2)]}

db3.re

let x = ref(0); // Equivalent to let x = toMut(0);
// let x: ref(int) = {contents: 0};

x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);
// - : int = 1

db4.re

type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);
// type prim = A | B(bool) | C(char) | D(int) | E(float) | F(string);

db5.re

let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};
// let change: mut(prim) =&gt; prim = &lt;fun&gt;;

db6.re

let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};
// let toString: mut(prim) =&gt; string = &lt;fun&gt;;

db7.re

let a = toMut(A); toString(a); a.value = change(a); toString(a);
// let a: mut(prim) = {value: A};
// - : string = &quot;empty&quot;
// - : string = &quot;empty&quot;

let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
// let b: mut(prim) = {value: B(false)};
// - : string = &quot;false&quot;
// - : string = &quot;true&quot;

let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
// let c: mut(prim) = {value: C(&#x27;a&#x27;)};
// - : string = &quot;a&quot;
// - : string = &quot;b&quot;

let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
// let d: mut(prim) = {value: D(0)};
// - : string = &quot;0&quot;
// - : string = &quot;+1&quot;

let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
// let e: mut(prim) = {value: E(0.)};
// - : string = &quot;0.&quot;
// - : string = &quot;+1.&quot;

let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);
// let f: mut(prim) = {value: F(&quot;Hello&quot;)};
// - : string = &quot;Hello&quot;
// - : string = &quot;Hello!&quot;

db8.re

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];
/*
let dbRaw: list(array((string, prim))) =
  [[|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(false))|],
   [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)),
     (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)),
     (&quot;alive&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|]];

*/

db9.re

module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});
// module StringMap: { ... };</code></pre><p>Structuring a strictly-typed database while ensuring all necessary keys are included and defaults are set for missing items:</p><pre><code>db.re

/* HANDLING PRIMITIVE TYPES */

// Mutability in ReasonML is a feature primarily used with records. Here&#x27;s how you define a mutable type that can hold any value:
type mut(&#x27;a) = {
  mutable value: &#x27;a,
};

// In λ-calculus, function types like f: A -&gt; B imply a transformation or proof from A to B. The functions toMut and fromMut serve as bridges between mutable and immutable types, showing they can be interchangeable:
let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;

// Using the standard implementation as a reference, you can see how it translates in practical terms:
let x = ref(0); // Equivalent to let x = toMut(0);
x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);

// ReasonML requires explicit type declarations for union types, unlike TypeScript where you might use &quot;int | null&quot;:
type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);

// Variant types in ReasonML, akin to sum types or dependent types in other languages, are exhaustive and unique, ensuring no overlap between types.

// Handling these types necessitates a switch statement, covering all possible variants for completeness:
let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};

// For pattern matching, especially when not all cases are addressed explicitly, the wildcard &quot;_&quot; can be a fallback. The &quot;when&quot; keyword allows for additional conditions in matches, offering a concise way to handle complex patterns:
let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};

// Testing different cases to demonstrate how these functions work with the defined types:
let a = toMut(A); toString(a); a.value = change(a); toString(a);
let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);

/* DATABASE STORAGE FOR DATA SCIENCE */

// Working with generic types and function handling is one thing, but let&#x27;s step into a scenario where the stakes are higher: being data scientists at a medical center, tasked with deriving basic statistics from patient data. Given a raw database in a text file format, we&#x27;ve managed to extract key information as follows:

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];

// The data&#x27;s format is row-wise with an arbitrary order, which could include duplicates, missing, or extra items. To streamline debugging, we&#x27;re aiming to cast these to string maps.

// Here&#x27;s where the Map.Make functor comes into play, allowing us to generate a StringMap keyed by strings for easier readability and manipulation, akin to handling JSON objects:
module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});

// Converting our map to a JSON-like string for debug-friendliness:
let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};

// Transitioning to a generic database format, our row-wise data gets a transformation. Here, we&#x27;re all about clarity and correctness:
let showJson = true;
let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);

// Accessing the elements becomes straightforward. Missing elements? No biggie, we handle that gracefully:
let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};

// After some exploration and analysis, key insights emerge regarding age, weight, name, and gender. These form the cornerstone of our new database signature:
type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};

// Structuring a strictly-typed database while ensuring all necessary keys are included and defaults are set for missing items:
let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);

// Finally, the database is correctly formatted. Next up, transposing this database to a column-wise format, ready for statistical analysis:
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};

// Successfully transposing our data, we&#x27;re set to dive deep into the analysis, equipped with a database that&#x27;s both comprehensive and accurately structured.
let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));

/* STATISTICS LIBRARY DEVELOPMENT */

// Venturing into building a generic statistics library, we&#x27;re focusing on versatility across different data structures. Whether dealing with Lists or Arrays, the goal is seamless integration and handling.

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
  
// The challenge lies in unpacking these varied structures into a consistent format, ideally a list of primitives, for statistical analysis. Given the evolving nature of our library, not all types are fully supported yet, leading to potential exceptions for unhandled cases.
exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};

// To ensure a smooth user experience, we wrap secToList in a function that gracefully handles exceptions, providing clear feedback rather than abrupt errors.
let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};

// Diving into the core of our library, we aim to offer basic but essential statistical functions, each designed to work with a specific type of data.

// getCounts tackles enumeration, mapping each unique string in a list to its frequency of occurrence, ideal for categorical data analysis.
let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}

// getMedian finds the middle value in a list of floats after sorting, a key measure of central tendency for quantitative data.
let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};

// getMean computes the average from a list of floats, providing a quick snapshot of your data&#x27;s central value.
let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));

// Structuring our output, we define types for summarizing string and float data, encapsulating counts for categorical data and central measures for continuous data.
type stringStats = {
  counts: list((string, int)),
};

type floatStats = {
  mean: float,
  median: float,
};

/* DATA ANALYSIS FRAMEWORK */

// Integrating complex data structures into actionable insights requires a systematic approach. We&#x27;ve established methods to deconstruct complex data into primitive lists and have statistical functions ready. The challenge now is to seamlessly connect these components.

// First, let&#x27;s categorize data types based on their analytical utility:

// - Nominal data, like colors &quot;Blue&quot; and &quot;Yellow&quot;, are distinct without a meaningful order. The mode serves as their central tendency measure.
// - Boolean data, a subset of nominal, consists of binary choices like &quot;Yes&quot; and &quot;No&quot;.
// - Ordinal data, such as ratings from 1 (&quot;Low&quot;) to 5 (&quot;High&quot;), imply order but not the uniformity of scale. Their median reflects central tendency.
// - Numeric data, representing continuous or interval data, can be fully quantified. The mean is used to express their central tendency.

// Recognizing that not all operations apply universally across data types underscores the importance of targeted analytical strategies.

// Transitioning to the implementation phase:

// The `listToFloat` function converts a list of primitives to floats, selectively allowing boolean and integer conversions based on flags:
let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};

// Converting primitives to strings while handling incompatible types by casting to floats, then stringifying, allows for flexible data interpretation:
exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};

// `getFloatStats` and `getStringStats` functions then process these lists into statistical summaries, considering the data level restrictions and debug options respectively:
let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}

// Finally, transforming primitive lists to the expected input format for statistical analysis:
let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));

// Extracting statistics becomes straightforward with prepped data:
let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);

// Now, it&#x27;s just a matter of calling the appropriate statistical function for each data type, with optional debugging for string conversions:
getStringStats(names, ~debug=true, ());
getFloatStats(weights, ~level=1, ());
getStringStats(weights, ~debug=true, ());

getFloatStats(ages, ~level=2, ());
getStringStats(ages, ~debug=true, ());

getFloatStats(males, ~level=3, ());
getStringStats(males, ~debug=true, ());

db1.re

type mut(&#x27;a) = {
  mutable value: &#x27;a,
};
// type mut(&#x27;a) = { mutable value: &#x27;a, };

db10.re

let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};
// let mapToJson: StringMap.t(prim) =&gt; string = &lt;fun&gt;;

db11.re

let showJson = true;
// let showJson: bool = true;

let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);
/* let dbGeneric: list(StringMap.t(prim)) =
  [&lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;];
*/
/*
{age: +18, male: false, name: Ada, weight: +98.5}
{age: +25, male: true, name: Ben, weight: +81.5}
{age: +45, alive: true, name: Caz, weight: +70.6}
{age: +10, male: true, name: Dan, weight: +98.5}
{male: false, name: Eve}
*/

db12.re

let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};
// let tryAccessDbGeneric: (StringMap.key, int) =&gt; prim = &lt;fun&gt;;

db13.re

type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};
// type signature = { age: prim, weight: prim, name: prim, male: prim, };

db14.re

let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);
/*
let db: list(signature) =
  [{age: D(18), weight: E(98.5), name: F(&quot;Ada&quot;), male: B(false)},
   {age: D(25), weight: E(81.5), name: F(&quot;Ben&quot;), male: B(true)},
   {age: D(45), weight: E(70.6), name: F(&quot;Caz&quot;), male: A},
   {age: D(10), weight: E(98.5), name: F(&quot;Dan&quot;), male: B(true)},
   {age: A, weight: A, name: F(&quot;Eve&quot;), male: B(false)}];
*/

db15.re

type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
/*
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
*/

db16.re

let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));
/*
let dbCol: signatureColWise =
  {ageList: [D(18), D(25), D(45), D(10), A],
   weightList: [E(98.5), E(81.5), E(70.6), E(98.5), A],
   nameList: [F(&quot;Ada&quot;), F(&quot;Ben&quot;), F(&quot;Caz&quot;), F(&quot;Dan&quot;), F(&quot;Eve&quot;)],
   maleList: [B(false), B(true), A, B(true), B(false)]};
*/

db17.re

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
/* 
type sec =
    G(prim)
  | H(list(sec))
  | I(array(sec))
  | J((string, sec))
  | K({ key: string, value: sec, });
*/

db18.re

exception Unimplemented_type(string);
// exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};
// let secToList: sec =&gt; list(prim) = &lt;fun&gt;;

db19.re

let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};
// let trySecToList: sec =&gt; list(prim) = &lt;fun&gt;;

db2.re

let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
// let toMut: &#x27;a =&gt; mut(&#x27;a) = &lt;fun&gt;;

let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;
// let fromMut: mut(&#x27;a) =&gt; &#x27;a = &lt;fun&gt;;

db20.re

let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}
// let getCounts: list(StringMap.key) =&gt; list((string, int)) = &lt;fun&gt;;

db21.re

let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};
// let getMedian: list(float) =&gt; float = &lt;fun&gt;;

db22.re

let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));
// let getMean: list(float) =&gt; float = &lt;fun&gt;;

db23.re

type stringStats = {
  counts: list((string, int)),
};
// type stringStats = { counts: list((string, int)), };

type floatStats = {
  mean: float,
  median: float,
};
// type floatStats = { mean: float, median: float, };

db24.re

let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};
/*
let listToFloat:
  (list(prim), ~boolAllowed: bool=?, ~intAllowed: bool=?, unit) =&gt; list(float) =
  &lt;fun&gt;;
*/

db25.re

exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};
// let listToString: (list(prim), ~debug: bool=?, unit) =&gt; list(string) = &lt;fun&gt;;

db26.re

let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};
// let getFloatStats: (sec, ~level: int=?, unit) =&gt; floatStats = &lt;fun&gt;;

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}
// let getStringStats: (sec, ~debug: bool=?, unit) =&gt; stringStats = &lt;fun&gt;;

db27.re

let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));
// let primListToSec: list(prim) =&gt; sec = &lt;fun&gt;;

db28.re

let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);
/*
let ages: sec = H([G((D(18))), G((D(25))), G((D(45))), G((D(10))), G(A)]);
let weights: sec =
  H([G((E(98.5))), G((E(81.5))), G((E(70.6))), G((E(98.5))), G(A)]);
let names: sec =
  H([G((F(&quot;Ada&quot;))), G((F(&quot;Ben&quot;))), G((F(&quot;Caz&quot;))), G((F(&quot;Dan&quot;))), G((F(&quot;Eve&quot;)))]);
let males: sec =
  H([G((B(false))), G((B(true))), G(A), G((B(true))), G((B(false)))]);
*/

db29.re

getStringStats(names, ~debug=true, ());
// - : stringStats = {counts: [(&quot;Ada&quot;, 1), (&quot;Ben&quot;, 1), (&quot;Caz&quot;, 1), (&quot;Dan&quot;, 1), (&quot;Eve&quot;, 1)]}

getFloatStats(weights, ~level=1, ());
// - : floatStats = {mean: 87.275, median: 90.}

getStringStats(weights, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;70.6&quot;, 1), (&quot;81.5&quot;, 1), (&quot;98.5&quot;, 2)]}

getFloatStats(ages, ~level=2, ());
// - : floatStats = {mean: 24.5, median: 21.5}

getStringStats(ages, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;10.&quot;, 1), (&quot;18.&quot;, 1), (&quot;25.&quot;, 1), (&quot;45.&quot;, 1)]}

getFloatStats(males, ~level=3, ());
// - : floatStats = {mean: 0.5, median: 0.5}

getStringStats(males, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;0.&quot;, 2), (&quot;1.&quot;, 2)]}

db3.re

let x = ref(0); // Equivalent to let x = toMut(0);
// let x: ref(int) = {contents: 0};

x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);
// - : int = 1

db4.re

type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);
// type prim = A | B(bool) | C(char) | D(int) | E(float) | F(string);

db5.re

let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};
// let change: mut(prim) =&gt; prim = &lt;fun&gt;;

db6.re

let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};
// let toString: mut(prim) =&gt; string = &lt;fun&gt;;

db7.re

let a = toMut(A); toString(a); a.value = change(a); toString(a);
// let a: mut(prim) = {value: A};
// - : string = &quot;empty&quot;
// - : string = &quot;empty&quot;

let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
// let b: mut(prim) = {value: B(false)};
// - : string = &quot;false&quot;
// - : string = &quot;true&quot;

let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
// let c: mut(prim) = {value: C(&#x27;a&#x27;)};
// - : string = &quot;a&quot;
// - : string = &quot;b&quot;

let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
// let d: mut(prim) = {value: D(0)};
// - : string = &quot;0&quot;
// - : string = &quot;+1&quot;

let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
// let e: mut(prim) = {value: E(0.)};
// - : string = &quot;0.&quot;
// - : string = &quot;+1.&quot;

let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);
// let f: mut(prim) = {value: F(&quot;Hello&quot;)};
// - : string = &quot;Hello&quot;
// - : string = &quot;Hello!&quot;

db8.re

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];
/*
let dbRaw: list(array((string, prim))) =
  [[|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(false))|],
   [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)),
     (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)),
     (&quot;alive&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|]];

*/

db9.re

module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});
// module StringMap: { ... };</code></pre><p>Finally, the database is correctly formatted. Next up, transposing this database to a column-wise format, ready for statistical analysis:</p><pre><code>db.re

/* HANDLING PRIMITIVE TYPES */

// Mutability in ReasonML is a feature primarily used with records. Here&#x27;s how you define a mutable type that can hold any value:
type mut(&#x27;a) = {
  mutable value: &#x27;a,
};

// In λ-calculus, function types like f: A -&gt; B imply a transformation or proof from A to B. The functions toMut and fromMut serve as bridges between mutable and immutable types, showing they can be interchangeable:
let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;

// Using the standard implementation as a reference, you can see how it translates in practical terms:
let x = ref(0); // Equivalent to let x = toMut(0);
x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);

// ReasonML requires explicit type declarations for union types, unlike TypeScript where you might use &quot;int | null&quot;:
type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);

// Variant types in ReasonML, akin to sum types or dependent types in other languages, are exhaustive and unique, ensuring no overlap between types.

// Handling these types necessitates a switch statement, covering all possible variants for completeness:
let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};

// For pattern matching, especially when not all cases are addressed explicitly, the wildcard &quot;_&quot; can be a fallback. The &quot;when&quot; keyword allows for additional conditions in matches, offering a concise way to handle complex patterns:
let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};

// Testing different cases to demonstrate how these functions work with the defined types:
let a = toMut(A); toString(a); a.value = change(a); toString(a);
let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);

/* DATABASE STORAGE FOR DATA SCIENCE */

// Working with generic types and function handling is one thing, but let&#x27;s step into a scenario where the stakes are higher: being data scientists at a medical center, tasked with deriving basic statistics from patient data. Given a raw database in a text file format, we&#x27;ve managed to extract key information as follows:

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];

// The data&#x27;s format is row-wise with an arbitrary order, which could include duplicates, missing, or extra items. To streamline debugging, we&#x27;re aiming to cast these to string maps.

// Here&#x27;s where the Map.Make functor comes into play, allowing us to generate a StringMap keyed by strings for easier readability and manipulation, akin to handling JSON objects:
module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});

// Converting our map to a JSON-like string for debug-friendliness:
let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};

// Transitioning to a generic database format, our row-wise data gets a transformation. Here, we&#x27;re all about clarity and correctness:
let showJson = true;
let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);

// Accessing the elements becomes straightforward. Missing elements? No biggie, we handle that gracefully:
let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};

// After some exploration and analysis, key insights emerge regarding age, weight, name, and gender. These form the cornerstone of our new database signature:
type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};

// Structuring a strictly-typed database while ensuring all necessary keys are included and defaults are set for missing items:
let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);

// Finally, the database is correctly formatted. Next up, transposing this database to a column-wise format, ready for statistical analysis:
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};

// Successfully transposing our data, we&#x27;re set to dive deep into the analysis, equipped with a database that&#x27;s both comprehensive and accurately structured.
let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));

/* STATISTICS LIBRARY DEVELOPMENT */

// Venturing into building a generic statistics library, we&#x27;re focusing on versatility across different data structures. Whether dealing with Lists or Arrays, the goal is seamless integration and handling.

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
  
// The challenge lies in unpacking these varied structures into a consistent format, ideally a list of primitives, for statistical analysis. Given the evolving nature of our library, not all types are fully supported yet, leading to potential exceptions for unhandled cases.
exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};

// To ensure a smooth user experience, we wrap secToList in a function that gracefully handles exceptions, providing clear feedback rather than abrupt errors.
let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};

// Diving into the core of our library, we aim to offer basic but essential statistical functions, each designed to work with a specific type of data.

// getCounts tackles enumeration, mapping each unique string in a list to its frequency of occurrence, ideal for categorical data analysis.
let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}

// getMedian finds the middle value in a list of floats after sorting, a key measure of central tendency for quantitative data.
let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};

// getMean computes the average from a list of floats, providing a quick snapshot of your data&#x27;s central value.
let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));

// Structuring our output, we define types for summarizing string and float data, encapsulating counts for categorical data and central measures for continuous data.
type stringStats = {
  counts: list((string, int)),
};

type floatStats = {
  mean: float,
  median: float,
};

/* DATA ANALYSIS FRAMEWORK */

// Integrating complex data structures into actionable insights requires a systematic approach. We&#x27;ve established methods to deconstruct complex data into primitive lists and have statistical functions ready. The challenge now is to seamlessly connect these components.

// First, let&#x27;s categorize data types based on their analytical utility:

// - Nominal data, like colors &quot;Blue&quot; and &quot;Yellow&quot;, are distinct without a meaningful order. The mode serves as their central tendency measure.
// - Boolean data, a subset of nominal, consists of binary choices like &quot;Yes&quot; and &quot;No&quot;.
// - Ordinal data, such as ratings from 1 (&quot;Low&quot;) to 5 (&quot;High&quot;), imply order but not the uniformity of scale. Their median reflects central tendency.
// - Numeric data, representing continuous or interval data, can be fully quantified. The mean is used to express their central tendency.

// Recognizing that not all operations apply universally across data types underscores the importance of targeted analytical strategies.

// Transitioning to the implementation phase:

// The `listToFloat` function converts a list of primitives to floats, selectively allowing boolean and integer conversions based on flags:
let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};

// Converting primitives to strings while handling incompatible types by casting to floats, then stringifying, allows for flexible data interpretation:
exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};

// `getFloatStats` and `getStringStats` functions then process these lists into statistical summaries, considering the data level restrictions and debug options respectively:
let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}

// Finally, transforming primitive lists to the expected input format for statistical analysis:
let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));

// Extracting statistics becomes straightforward with prepped data:
let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);

// Now, it&#x27;s just a matter of calling the appropriate statistical function for each data type, with optional debugging for string conversions:
getStringStats(names, ~debug=true, ());
getFloatStats(weights, ~level=1, ());
getStringStats(weights, ~debug=true, ());

getFloatStats(ages, ~level=2, ());
getStringStats(ages, ~debug=true, ());

getFloatStats(males, ~level=3, ());
getStringStats(males, ~debug=true, ());

db1.re

type mut(&#x27;a) = {
  mutable value: &#x27;a,
};
// type mut(&#x27;a) = { mutable value: &#x27;a, };

db10.re

let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};
// let mapToJson: StringMap.t(prim) =&gt; string = &lt;fun&gt;;

db11.re

let showJson = true;
// let showJson: bool = true;

let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);
/* let dbGeneric: list(StringMap.t(prim)) =
  [&lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;];
*/
/*
{age: +18, male: false, name: Ada, weight: +98.5}
{age: +25, male: true, name: Ben, weight: +81.5}
{age: +45, alive: true, name: Caz, weight: +70.6}
{age: +10, male: true, name: Dan, weight: +98.5}
{male: false, name: Eve}
*/

db12.re

let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};
// let tryAccessDbGeneric: (StringMap.key, int) =&gt; prim = &lt;fun&gt;;

db13.re

type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};
// type signature = { age: prim, weight: prim, name: prim, male: prim, };

db14.re

let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);
/*
let db: list(signature) =
  [{age: D(18), weight: E(98.5), name: F(&quot;Ada&quot;), male: B(false)},
   {age: D(25), weight: E(81.5), name: F(&quot;Ben&quot;), male: B(true)},
   {age: D(45), weight: E(70.6), name: F(&quot;Caz&quot;), male: A},
   {age: D(10), weight: E(98.5), name: F(&quot;Dan&quot;), male: B(true)},
   {age: A, weight: A, name: F(&quot;Eve&quot;), male: B(false)}];
*/

db15.re

type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
/*
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
*/

db16.re

let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));
/*
let dbCol: signatureColWise =
  {ageList: [D(18), D(25), D(45), D(10), A],
   weightList: [E(98.5), E(81.5), E(70.6), E(98.5), A],
   nameList: [F(&quot;Ada&quot;), F(&quot;Ben&quot;), F(&quot;Caz&quot;), F(&quot;Dan&quot;), F(&quot;Eve&quot;)],
   maleList: [B(false), B(true), A, B(true), B(false)]};
*/

db17.re

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
/* 
type sec =
    G(prim)
  | H(list(sec))
  | I(array(sec))
  | J((string, sec))
  | K({ key: string, value: sec, });
*/

db18.re

exception Unimplemented_type(string);
// exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};
// let secToList: sec =&gt; list(prim) = &lt;fun&gt;;

db19.re

let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};
// let trySecToList: sec =&gt; list(prim) = &lt;fun&gt;;

db2.re

let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
// let toMut: &#x27;a =&gt; mut(&#x27;a) = &lt;fun&gt;;

let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;
// let fromMut: mut(&#x27;a) =&gt; &#x27;a = &lt;fun&gt;;

db20.re

let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}
// let getCounts: list(StringMap.key) =&gt; list((string, int)) = &lt;fun&gt;;

db21.re

let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};
// let getMedian: list(float) =&gt; float = &lt;fun&gt;;

db22.re

let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));
// let getMean: list(float) =&gt; float = &lt;fun&gt;;

db23.re

type stringStats = {
  counts: list((string, int)),
};
// type stringStats = { counts: list((string, int)), };

type floatStats = {
  mean: float,
  median: float,
};
// type floatStats = { mean: float, median: float, };

db24.re

let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};
/*
let listToFloat:
  (list(prim), ~boolAllowed: bool=?, ~intAllowed: bool=?, unit) =&gt; list(float) =
  &lt;fun&gt;;
*/

db25.re

exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};
// let listToString: (list(prim), ~debug: bool=?, unit) =&gt; list(string) = &lt;fun&gt;;

db26.re

let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};
// let getFloatStats: (sec, ~level: int=?, unit) =&gt; floatStats = &lt;fun&gt;;

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}
// let getStringStats: (sec, ~debug: bool=?, unit) =&gt; stringStats = &lt;fun&gt;;

db27.re

let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));
// let primListToSec: list(prim) =&gt; sec = &lt;fun&gt;;

db28.re

let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);
/*
let ages: sec = H([G((D(18))), G((D(25))), G((D(45))), G((D(10))), G(A)]);
let weights: sec =
  H([G((E(98.5))), G((E(81.5))), G((E(70.6))), G((E(98.5))), G(A)]);
let names: sec =
  H([G((F(&quot;Ada&quot;))), G((F(&quot;Ben&quot;))), G((F(&quot;Caz&quot;))), G((F(&quot;Dan&quot;))), G((F(&quot;Eve&quot;)))]);
let males: sec =
  H([G((B(false))), G((B(true))), G(A), G((B(true))), G((B(false)))]);
*/

db29.re

getStringStats(names, ~debug=true, ());
// - : stringStats = {counts: [(&quot;Ada&quot;, 1), (&quot;Ben&quot;, 1), (&quot;Caz&quot;, 1), (&quot;Dan&quot;, 1), (&quot;Eve&quot;, 1)]}

getFloatStats(weights, ~level=1, ());
// - : floatStats = {mean: 87.275, median: 90.}

getStringStats(weights, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;70.6&quot;, 1), (&quot;81.5&quot;, 1), (&quot;98.5&quot;, 2)]}

getFloatStats(ages, ~level=2, ());
// - : floatStats = {mean: 24.5, median: 21.5}

getStringStats(ages, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;10.&quot;, 1), (&quot;18.&quot;, 1), (&quot;25.&quot;, 1), (&quot;45.&quot;, 1)]}

getFloatStats(males, ~level=3, ());
// - : floatStats = {mean: 0.5, median: 0.5}

getStringStats(males, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;0.&quot;, 2), (&quot;1.&quot;, 2)]}

db3.re

let x = ref(0); // Equivalent to let x = toMut(0);
// let x: ref(int) = {contents: 0};

x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);
// - : int = 1

db4.re

type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);
// type prim = A | B(bool) | C(char) | D(int) | E(float) | F(string);

db5.re

let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};
// let change: mut(prim) =&gt; prim = &lt;fun&gt;;

db6.re

let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};
// let toString: mut(prim) =&gt; string = &lt;fun&gt;;

db7.re

let a = toMut(A); toString(a); a.value = change(a); toString(a);
// let a: mut(prim) = {value: A};
// - : string = &quot;empty&quot;
// - : string = &quot;empty&quot;

let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
// let b: mut(prim) = {value: B(false)};
// - : string = &quot;false&quot;
// - : string = &quot;true&quot;

let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
// let c: mut(prim) = {value: C(&#x27;a&#x27;)};
// - : string = &quot;a&quot;
// - : string = &quot;b&quot;

let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
// let d: mut(prim) = {value: D(0)};
// - : string = &quot;0&quot;
// - : string = &quot;+1&quot;

let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
// let e: mut(prim) = {value: E(0.)};
// - : string = &quot;0.&quot;
// - : string = &quot;+1.&quot;

let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);
// let f: mut(prim) = {value: F(&quot;Hello&quot;)};
// - : string = &quot;Hello&quot;
// - : string = &quot;Hello!&quot;

db8.re

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];
/*
let dbRaw: list(array((string, prim))) =
  [[|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(false))|],
   [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)),
     (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)),
     (&quot;alive&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|]];

*/

db9.re

module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});
// module StringMap: { ... };</code></pre><p>Successfully transposing our data, we’re set to dive deep into the analysis, equipped with a database that’s both comprehensive and accurately structured.</p><pre><code>db.re

/* HANDLING PRIMITIVE TYPES */

// Mutability in ReasonML is a feature primarily used with records. Here&#x27;s how you define a mutable type that can hold any value:
type mut(&#x27;a) = {
  mutable value: &#x27;a,
};

// In λ-calculus, function types like f: A -&gt; B imply a transformation or proof from A to B. The functions toMut and fromMut serve as bridges between mutable and immutable types, showing they can be interchangeable:
let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;

// Using the standard implementation as a reference, you can see how it translates in practical terms:
let x = ref(0); // Equivalent to let x = toMut(0);
x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);

// ReasonML requires explicit type declarations for union types, unlike TypeScript where you might use &quot;int | null&quot;:
type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);

// Variant types in ReasonML, akin to sum types or dependent types in other languages, are exhaustive and unique, ensuring no overlap between types.

// Handling these types necessitates a switch statement, covering all possible variants for completeness:
let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};

// For pattern matching, especially when not all cases are addressed explicitly, the wildcard &quot;_&quot; can be a fallback. The &quot;when&quot; keyword allows for additional conditions in matches, offering a concise way to handle complex patterns:
let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};

// Testing different cases to demonstrate how these functions work with the defined types:
let a = toMut(A); toString(a); a.value = change(a); toString(a);
let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);

/* DATABASE STORAGE FOR DATA SCIENCE */

// Working with generic types and function handling is one thing, but let&#x27;s step into a scenario where the stakes are higher: being data scientists at a medical center, tasked with deriving basic statistics from patient data. Given a raw database in a text file format, we&#x27;ve managed to extract key information as follows:

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];

// The data&#x27;s format is row-wise with an arbitrary order, which could include duplicates, missing, or extra items. To streamline debugging, we&#x27;re aiming to cast these to string maps.

// Here&#x27;s where the Map.Make functor comes into play, allowing us to generate a StringMap keyed by strings for easier readability and manipulation, akin to handling JSON objects:
module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});

// Converting our map to a JSON-like string for debug-friendliness:
let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};

// Transitioning to a generic database format, our row-wise data gets a transformation. Here, we&#x27;re all about clarity and correctness:
let showJson = true;
let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);

// Accessing the elements becomes straightforward. Missing elements? No biggie, we handle that gracefully:
let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};

// After some exploration and analysis, key insights emerge regarding age, weight, name, and gender. These form the cornerstone of our new database signature:
type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};

// Structuring a strictly-typed database while ensuring all necessary keys are included and defaults are set for missing items:
let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);

// Finally, the database is correctly formatted. Next up, transposing this database to a column-wise format, ready for statistical analysis:
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};

// Successfully transposing our data, we&#x27;re set to dive deep into the analysis, equipped with a database that&#x27;s both comprehensive and accurately structured.
let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));

/* STATISTICS LIBRARY DEVELOPMENT */

// Venturing into building a generic statistics library, we&#x27;re focusing on versatility across different data structures. Whether dealing with Lists or Arrays, the goal is seamless integration and handling.

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
  
// The challenge lies in unpacking these varied structures into a consistent format, ideally a list of primitives, for statistical analysis. Given the evolving nature of our library, not all types are fully supported yet, leading to potential exceptions for unhandled cases.
exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};

// To ensure a smooth user experience, we wrap secToList in a function that gracefully handles exceptions, providing clear feedback rather than abrupt errors.
let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};

// Diving into the core of our library, we aim to offer basic but essential statistical functions, each designed to work with a specific type of data.

// getCounts tackles enumeration, mapping each unique string in a list to its frequency of occurrence, ideal for categorical data analysis.
let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}

// getMedian finds the middle value in a list of floats after sorting, a key measure of central tendency for quantitative data.
let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};

// getMean computes the average from a list of floats, providing a quick snapshot of your data&#x27;s central value.
let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));

// Structuring our output, we define types for summarizing string and float data, encapsulating counts for categorical data and central measures for continuous data.
type stringStats = {
  counts: list((string, int)),
};

type floatStats = {
  mean: float,
  median: float,
};

/* DATA ANALYSIS FRAMEWORK */

// Integrating complex data structures into actionable insights requires a systematic approach. We&#x27;ve established methods to deconstruct complex data into primitive lists and have statistical functions ready. The challenge now is to seamlessly connect these components.

// First, let&#x27;s categorize data types based on their analytical utility:

// - Nominal data, like colors &quot;Blue&quot; and &quot;Yellow&quot;, are distinct without a meaningful order. The mode serves as their central tendency measure.
// - Boolean data, a subset of nominal, consists of binary choices like &quot;Yes&quot; and &quot;No&quot;.
// - Ordinal data, such as ratings from 1 (&quot;Low&quot;) to 5 (&quot;High&quot;), imply order but not the uniformity of scale. Their median reflects central tendency.
// - Numeric data, representing continuous or interval data, can be fully quantified. The mean is used to express their central tendency.

// Recognizing that not all operations apply universally across data types underscores the importance of targeted analytical strategies.

// Transitioning to the implementation phase:

// The `listToFloat` function converts a list of primitives to floats, selectively allowing boolean and integer conversions based on flags:
let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};

// Converting primitives to strings while handling incompatible types by casting to floats, then stringifying, allows for flexible data interpretation:
exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};

// `getFloatStats` and `getStringStats` functions then process these lists into statistical summaries, considering the data level restrictions and debug options respectively:
let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}

// Finally, transforming primitive lists to the expected input format for statistical analysis:
let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));

// Extracting statistics becomes straightforward with prepped data:
let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);

// Now, it&#x27;s just a matter of calling the appropriate statistical function for each data type, with optional debugging for string conversions:
getStringStats(names, ~debug=true, ());
getFloatStats(weights, ~level=1, ());
getStringStats(weights, ~debug=true, ());

getFloatStats(ages, ~level=2, ());
getStringStats(ages, ~debug=true, ());

getFloatStats(males, ~level=3, ());
getStringStats(males, ~debug=true, ());

db1.re

type mut(&#x27;a) = {
  mutable value: &#x27;a,
};
// type mut(&#x27;a) = { mutable value: &#x27;a, };

db10.re

let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};
// let mapToJson: StringMap.t(prim) =&gt; string = &lt;fun&gt;;

db11.re

let showJson = true;
// let showJson: bool = true;

let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);
/* let dbGeneric: list(StringMap.t(prim)) =
  [&lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;];
*/
/*
{age: +18, male: false, name: Ada, weight: +98.5}
{age: +25, male: true, name: Ben, weight: +81.5}
{age: +45, alive: true, name: Caz, weight: +70.6}
{age: +10, male: true, name: Dan, weight: +98.5}
{male: false, name: Eve}
*/

db12.re

let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};
// let tryAccessDbGeneric: (StringMap.key, int) =&gt; prim = &lt;fun&gt;;

db13.re

type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};
// type signature = { age: prim, weight: prim, name: prim, male: prim, };

db14.re

let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);
/*
let db: list(signature) =
  [{age: D(18), weight: E(98.5), name: F(&quot;Ada&quot;), male: B(false)},
   {age: D(25), weight: E(81.5), name: F(&quot;Ben&quot;), male: B(true)},
   {age: D(45), weight: E(70.6), name: F(&quot;Caz&quot;), male: A},
   {age: D(10), weight: E(98.5), name: F(&quot;Dan&quot;), male: B(true)},
   {age: A, weight: A, name: F(&quot;Eve&quot;), male: B(false)}];
*/

db15.re

type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
/*
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
*/

db16.re

let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));
/*
let dbCol: signatureColWise =
  {ageList: [D(18), D(25), D(45), D(10), A],
   weightList: [E(98.5), E(81.5), E(70.6), E(98.5), A],
   nameList: [F(&quot;Ada&quot;), F(&quot;Ben&quot;), F(&quot;Caz&quot;), F(&quot;Dan&quot;), F(&quot;Eve&quot;)],
   maleList: [B(false), B(true), A, B(true), B(false)]};
*/

db17.re

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
/* 
type sec =
    G(prim)
  | H(list(sec))
  | I(array(sec))
  | J((string, sec))
  | K({ key: string, value: sec, });
*/

db18.re

exception Unimplemented_type(string);
// exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};
// let secToList: sec =&gt; list(prim) = &lt;fun&gt;;

db19.re

let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};
// let trySecToList: sec =&gt; list(prim) = &lt;fun&gt;;

db2.re

let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
// let toMut: &#x27;a =&gt; mut(&#x27;a) = &lt;fun&gt;;

let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;
// let fromMut: mut(&#x27;a) =&gt; &#x27;a = &lt;fun&gt;;

db20.re

let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}
// let getCounts: list(StringMap.key) =&gt; list((string, int)) = &lt;fun&gt;;

db21.re

let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};
// let getMedian: list(float) =&gt; float = &lt;fun&gt;;

db22.re

let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));
// let getMean: list(float) =&gt; float = &lt;fun&gt;;

db23.re

type stringStats = {
  counts: list((string, int)),
};
// type stringStats = { counts: list((string, int)), };

type floatStats = {
  mean: float,
  median: float,
};
// type floatStats = { mean: float, median: float, };

db24.re

let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};
/*
let listToFloat:
  (list(prim), ~boolAllowed: bool=?, ~intAllowed: bool=?, unit) =&gt; list(float) =
  &lt;fun&gt;;
*/

db25.re

exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};
// let listToString: (list(prim), ~debug: bool=?, unit) =&gt; list(string) = &lt;fun&gt;;

db26.re

let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};
// let getFloatStats: (sec, ~level: int=?, unit) =&gt; floatStats = &lt;fun&gt;;

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}
// let getStringStats: (sec, ~debug: bool=?, unit) =&gt; stringStats = &lt;fun&gt;;

db27.re

let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));
// let primListToSec: list(prim) =&gt; sec = &lt;fun&gt;;

db28.re

let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);
/*
let ages: sec = H([G((D(18))), G((D(25))), G((D(45))), G((D(10))), G(A)]);
let weights: sec =
  H([G((E(98.5))), G((E(81.5))), G((E(70.6))), G((E(98.5))), G(A)]);
let names: sec =
  H([G((F(&quot;Ada&quot;))), G((F(&quot;Ben&quot;))), G((F(&quot;Caz&quot;))), G((F(&quot;Dan&quot;))), G((F(&quot;Eve&quot;)))]);
let males: sec =
  H([G((B(false))), G((B(true))), G(A), G((B(true))), G((B(false)))]);
*/

db29.re

getStringStats(names, ~debug=true, ());
// - : stringStats = {counts: [(&quot;Ada&quot;, 1), (&quot;Ben&quot;, 1), (&quot;Caz&quot;, 1), (&quot;Dan&quot;, 1), (&quot;Eve&quot;, 1)]}

getFloatStats(weights, ~level=1, ());
// - : floatStats = {mean: 87.275, median: 90.}

getStringStats(weights, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;70.6&quot;, 1), (&quot;81.5&quot;, 1), (&quot;98.5&quot;, 2)]}

getFloatStats(ages, ~level=2, ());
// - : floatStats = {mean: 24.5, median: 21.5}

getStringStats(ages, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;10.&quot;, 1), (&quot;18.&quot;, 1), (&quot;25.&quot;, 1), (&quot;45.&quot;, 1)]}

getFloatStats(males, ~level=3, ());
// - : floatStats = {mean: 0.5, median: 0.5}

getStringStats(males, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;0.&quot;, 2), (&quot;1.&quot;, 2)]}

db3.re

let x = ref(0); // Equivalent to let x = toMut(0);
// let x: ref(int) = {contents: 0};

x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);
// - : int = 1

db4.re

type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);
// type prim = A | B(bool) | C(char) | D(int) | E(float) | F(string);

db5.re

let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};
// let change: mut(prim) =&gt; prim = &lt;fun&gt;;

db6.re

let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};
// let toString: mut(prim) =&gt; string = &lt;fun&gt;;

db7.re

let a = toMut(A); toString(a); a.value = change(a); toString(a);
// let a: mut(prim) = {value: A};
// - : string = &quot;empty&quot;
// - : string = &quot;empty&quot;

let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
// let b: mut(prim) = {value: B(false)};
// - : string = &quot;false&quot;
// - : string = &quot;true&quot;

let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
// let c: mut(prim) = {value: C(&#x27;a&#x27;)};
// - : string = &quot;a&quot;
// - : string = &quot;b&quot;

let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
// let d: mut(prim) = {value: D(0)};
// - : string = &quot;0&quot;
// - : string = &quot;+1&quot;

let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
// let e: mut(prim) = {value: E(0.)};
// - : string = &quot;0.&quot;
// - : string = &quot;+1.&quot;

let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);
// let f: mut(prim) = {value: F(&quot;Hello&quot;)};
// - : string = &quot;Hello&quot;
// - : string = &quot;Hello!&quot;

db8.re

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];
/*
let dbRaw: list(array((string, prim))) =
  [[|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(false))|],
   [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)),
     (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)),
     (&quot;alive&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|]];

*/

db9.re

module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});
// module StringMap: { ... };</code></pre><h4>Statistics Library</h4><figure><img alt="" src="https://cdn-images-1.medium.com/max/1400/1*GHWalGwAu9NR3dGDGD-zew.png" /><figcaption>Source: What is the difference between pandas “describe” and “describe()”?, Stack Overflow</figcaption></figure><p>Venturing into building a generic statistics library, we’re focusing on versatility across different data structures. Whether dealing with Lists or Arrays, the goal is seamless integration and handling.</p><pre><code>db.re

/* HANDLING PRIMITIVE TYPES */

// Mutability in ReasonML is a feature primarily used with records. Here&#x27;s how you define a mutable type that can hold any value:
type mut(&#x27;a) = {
  mutable value: &#x27;a,
};

// In λ-calculus, function types like f: A -&gt; B imply a transformation or proof from A to B. The functions toMut and fromMut serve as bridges between mutable and immutable types, showing they can be interchangeable:
let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;

// Using the standard implementation as a reference, you can see how it translates in practical terms:
let x = ref(0); // Equivalent to let x = toMut(0);
x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);

// ReasonML requires explicit type declarations for union types, unlike TypeScript where you might use &quot;int | null&quot;:
type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);

// Variant types in ReasonML, akin to sum types or dependent types in other languages, are exhaustive and unique, ensuring no overlap between types.

// Handling these types necessitates a switch statement, covering all possible variants for completeness:
let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};

// For pattern matching, especially when not all cases are addressed explicitly, the wildcard &quot;_&quot; can be a fallback. The &quot;when&quot; keyword allows for additional conditions in matches, offering a concise way to handle complex patterns:
let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};

// Testing different cases to demonstrate how these functions work with the defined types:
let a = toMut(A); toString(a); a.value = change(a); toString(a);
let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);

/* DATABASE STORAGE FOR DATA SCIENCE */

// Working with generic types and function handling is one thing, but let&#x27;s step into a scenario where the stakes are higher: being data scientists at a medical center, tasked with deriving basic statistics from patient data. Given a raw database in a text file format, we&#x27;ve managed to extract key information as follows:

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];

// The data&#x27;s format is row-wise with an arbitrary order, which could include duplicates, missing, or extra items. To streamline debugging, we&#x27;re aiming to cast these to string maps.

// Here&#x27;s where the Map.Make functor comes into play, allowing us to generate a StringMap keyed by strings for easier readability and manipulation, akin to handling JSON objects:
module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});

// Converting our map to a JSON-like string for debug-friendliness:
let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};

// Transitioning to a generic database format, our row-wise data gets a transformation. Here, we&#x27;re all about clarity and correctness:
let showJson = true;
let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);

// Accessing the elements becomes straightforward. Missing elements? No biggie, we handle that gracefully:
let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};

// After some exploration and analysis, key insights emerge regarding age, weight, name, and gender. These form the cornerstone of our new database signature:
type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};

// Structuring a strictly-typed database while ensuring all necessary keys are included and defaults are set for missing items:
let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);

// Finally, the database is correctly formatted. Next up, transposing this database to a column-wise format, ready for statistical analysis:
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};

// Successfully transposing our data, we&#x27;re set to dive deep into the analysis, equipped with a database that&#x27;s both comprehensive and accurately structured.
let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));

/* STATISTICS LIBRARY DEVELOPMENT */

// Venturing into building a generic statistics library, we&#x27;re focusing on versatility across different data structures. Whether dealing with Lists or Arrays, the goal is seamless integration and handling.

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
  
// The challenge lies in unpacking these varied structures into a consistent format, ideally a list of primitives, for statistical analysis. Given the evolving nature of our library, not all types are fully supported yet, leading to potential exceptions for unhandled cases.
exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};

// To ensure a smooth user experience, we wrap secToList in a function that gracefully handles exceptions, providing clear feedback rather than abrupt errors.
let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};

// Diving into the core of our library, we aim to offer basic but essential statistical functions, each designed to work with a specific type of data.

// getCounts tackles enumeration, mapping each unique string in a list to its frequency of occurrence, ideal for categorical data analysis.
let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}

// getMedian finds the middle value in a list of floats after sorting, a key measure of central tendency for quantitative data.
let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};

// getMean computes the average from a list of floats, providing a quick snapshot of your data&#x27;s central value.
let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));

// Structuring our output, we define types for summarizing string and float data, encapsulating counts for categorical data and central measures for continuous data.
type stringStats = {
  counts: list((string, int)),
};

type floatStats = {
  mean: float,
  median: float,
};

/* DATA ANALYSIS FRAMEWORK */

// Integrating complex data structures into actionable insights requires a systematic approach. We&#x27;ve established methods to deconstruct complex data into primitive lists and have statistical functions ready. The challenge now is to seamlessly connect these components.

// First, let&#x27;s categorize data types based on their analytical utility:

// - Nominal data, like colors &quot;Blue&quot; and &quot;Yellow&quot;, are distinct without a meaningful order. The mode serves as their central tendency measure.
// - Boolean data, a subset of nominal, consists of binary choices like &quot;Yes&quot; and &quot;No&quot;.
// - Ordinal data, such as ratings from 1 (&quot;Low&quot;) to 5 (&quot;High&quot;), imply order but not the uniformity of scale. Their median reflects central tendency.
// - Numeric data, representing continuous or interval data, can be fully quantified. The mean is used to express their central tendency.

// Recognizing that not all operations apply universally across data types underscores the importance of targeted analytical strategies.

// Transitioning to the implementation phase:

// The `listToFloat` function converts a list of primitives to floats, selectively allowing boolean and integer conversions based on flags:
let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};

// Converting primitives to strings while handling incompatible types by casting to floats, then stringifying, allows for flexible data interpretation:
exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};

// `getFloatStats` and `getStringStats` functions then process these lists into statistical summaries, considering the data level restrictions and debug options respectively:
let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}

// Finally, transforming primitive lists to the expected input format for statistical analysis:
let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));

// Extracting statistics becomes straightforward with prepped data:
let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);

// Now, it&#x27;s just a matter of calling the appropriate statistical function for each data type, with optional debugging for string conversions:
getStringStats(names, ~debug=true, ());
getFloatStats(weights, ~level=1, ());
getStringStats(weights, ~debug=true, ());

getFloatStats(ages, ~level=2, ());
getStringStats(ages, ~debug=true, ());

getFloatStats(males, ~level=3, ());
getStringStats(males, ~debug=true, ());

db1.re

type mut(&#x27;a) = {
  mutable value: &#x27;a,
};
// type mut(&#x27;a) = { mutable value: &#x27;a, };

db10.re

let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};
// let mapToJson: StringMap.t(prim) =&gt; string = &lt;fun&gt;;

db11.re

let showJson = true;
// let showJson: bool = true;

let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);
/* let dbGeneric: list(StringMap.t(prim)) =
  [&lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;];
*/
/*
{age: +18, male: false, name: Ada, weight: +98.5}
{age: +25, male: true, name: Ben, weight: +81.5}
{age: +45, alive: true, name: Caz, weight: +70.6}
{age: +10, male: true, name: Dan, weight: +98.5}
{male: false, name: Eve}
*/

db12.re

let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};
// let tryAccessDbGeneric: (StringMap.key, int) =&gt; prim = &lt;fun&gt;;

db13.re

type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};
// type signature = { age: prim, weight: prim, name: prim, male: prim, };

db14.re

let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);
/*
let db: list(signature) =
  [{age: D(18), weight: E(98.5), name: F(&quot;Ada&quot;), male: B(false)},
   {age: D(25), weight: E(81.5), name: F(&quot;Ben&quot;), male: B(true)},
   {age: D(45), weight: E(70.6), name: F(&quot;Caz&quot;), male: A},
   {age: D(10), weight: E(98.5), name: F(&quot;Dan&quot;), male: B(true)},
   {age: A, weight: A, name: F(&quot;Eve&quot;), male: B(false)}];
*/

db15.re

type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
/*
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
*/

db16.re

let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));
/*
let dbCol: signatureColWise =
  {ageList: [D(18), D(25), D(45), D(10), A],
   weightList: [E(98.5), E(81.5), E(70.6), E(98.5), A],
   nameList: [F(&quot;Ada&quot;), F(&quot;Ben&quot;), F(&quot;Caz&quot;), F(&quot;Dan&quot;), F(&quot;Eve&quot;)],
   maleList: [B(false), B(true), A, B(true), B(false)]};
*/

db17.re

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
/* 
type sec =
    G(prim)
  | H(list(sec))
  | I(array(sec))
  | J((string, sec))
  | K({ key: string, value: sec, });
*/

db18.re

exception Unimplemented_type(string);
// exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};
// let secToList: sec =&gt; list(prim) = &lt;fun&gt;;

db19.re

let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};
// let trySecToList: sec =&gt; list(prim) = &lt;fun&gt;;

db2.re

let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
// let toMut: &#x27;a =&gt; mut(&#x27;a) = &lt;fun&gt;;

let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;
// let fromMut: mut(&#x27;a) =&gt; &#x27;a = &lt;fun&gt;;

db20.re

let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}
// let getCounts: list(StringMap.key) =&gt; list((string, int)) = &lt;fun&gt;;

db21.re

let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};
// let getMedian: list(float) =&gt; float = &lt;fun&gt;;

db22.re

let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));
// let getMean: list(float) =&gt; float = &lt;fun&gt;;

db23.re

type stringStats = {
  counts: list((string, int)),
};
// type stringStats = { counts: list((string, int)), };

type floatStats = {
  mean: float,
  median: float,
};
// type floatStats = { mean: float, median: float, };

db24.re

let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};
/*
let listToFloat:
  (list(prim), ~boolAllowed: bool=?, ~intAllowed: bool=?, unit) =&gt; list(float) =
  &lt;fun&gt;;
*/

db25.re

exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};
// let listToString: (list(prim), ~debug: bool=?, unit) =&gt; list(string) = &lt;fun&gt;;

db26.re

let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};
// let getFloatStats: (sec, ~level: int=?, unit) =&gt; floatStats = &lt;fun&gt;;

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}
// let getStringStats: (sec, ~debug: bool=?, unit) =&gt; stringStats = &lt;fun&gt;;

db27.re

let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));
// let primListToSec: list(prim) =&gt; sec = &lt;fun&gt;;

db28.re

let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);
/*
let ages: sec = H([G((D(18))), G((D(25))), G((D(45))), G((D(10))), G(A)]);
let weights: sec =
  H([G((E(98.5))), G((E(81.5))), G((E(70.6))), G((E(98.5))), G(A)]);
let names: sec =
  H([G((F(&quot;Ada&quot;))), G((F(&quot;Ben&quot;))), G((F(&quot;Caz&quot;))), G((F(&quot;Dan&quot;))), G((F(&quot;Eve&quot;)))]);
let males: sec =
  H([G((B(false))), G((B(true))), G(A), G((B(true))), G((B(false)))]);
*/

db29.re

getStringStats(names, ~debug=true, ());
// - : stringStats = {counts: [(&quot;Ada&quot;, 1), (&quot;Ben&quot;, 1), (&quot;Caz&quot;, 1), (&quot;Dan&quot;, 1), (&quot;Eve&quot;, 1)]}

getFloatStats(weights, ~level=1, ());
// - : floatStats = {mean: 87.275, median: 90.}

getStringStats(weights, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;70.6&quot;, 1), (&quot;81.5&quot;, 1), (&quot;98.5&quot;, 2)]}

getFloatStats(ages, ~level=2, ());
// - : floatStats = {mean: 24.5, median: 21.5}

getStringStats(ages, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;10.&quot;, 1), (&quot;18.&quot;, 1), (&quot;25.&quot;, 1), (&quot;45.&quot;, 1)]}

getFloatStats(males, ~level=3, ());
// - : floatStats = {mean: 0.5, median: 0.5}

getStringStats(males, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;0.&quot;, 2), (&quot;1.&quot;, 2)]}

db3.re

let x = ref(0); // Equivalent to let x = toMut(0);
// let x: ref(int) = {contents: 0};

x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);
// - : int = 1

db4.re

type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);
// type prim = A | B(bool) | C(char) | D(int) | E(float) | F(string);

db5.re

let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};
// let change: mut(prim) =&gt; prim = &lt;fun&gt;;

db6.re

let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};
// let toString: mut(prim) =&gt; string = &lt;fun&gt;;

db7.re

let a = toMut(A); toString(a); a.value = change(a); toString(a);
// let a: mut(prim) = {value: A};
// - : string = &quot;empty&quot;
// - : string = &quot;empty&quot;

let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
// let b: mut(prim) = {value: B(false)};
// - : string = &quot;false&quot;
// - : string = &quot;true&quot;

let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
// let c: mut(prim) = {value: C(&#x27;a&#x27;)};
// - : string = &quot;a&quot;
// - : string = &quot;b&quot;

let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
// let d: mut(prim) = {value: D(0)};
// - : string = &quot;0&quot;
// - : string = &quot;+1&quot;

let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
// let e: mut(prim) = {value: E(0.)};
// - : string = &quot;0.&quot;
// - : string = &quot;+1.&quot;

let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);
// let f: mut(prim) = {value: F(&quot;Hello&quot;)};
// - : string = &quot;Hello&quot;
// - : string = &quot;Hello!&quot;

db8.re

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];
/*
let dbRaw: list(array((string, prim))) =
  [[|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(false))|],
   [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)),
     (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)),
     (&quot;alive&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|]];

*/

db9.re

module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});
// module StringMap: { ... };</code></pre><p>The challenge lies in unpacking these varied structures into a consistent format, ideally a list of primitives, for statistical analysis. Given the evolving nature of our library, not all types are fully supported yet, leading to potential exceptions for unhandled cases.</p><pre><code>db.re

/* HANDLING PRIMITIVE TYPES */

// Mutability in ReasonML is a feature primarily used with records. Here&#x27;s how you define a mutable type that can hold any value:
type mut(&#x27;a) = {
  mutable value: &#x27;a,
};

// In λ-calculus, function types like f: A -&gt; B imply a transformation or proof from A to B. The functions toMut and fromMut serve as bridges between mutable and immutable types, showing they can be interchangeable:
let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;

// Using the standard implementation as a reference, you can see how it translates in practical terms:
let x = ref(0); // Equivalent to let x = toMut(0);
x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);

// ReasonML requires explicit type declarations for union types, unlike TypeScript where you might use &quot;int | null&quot;:
type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);

// Variant types in ReasonML, akin to sum types or dependent types in other languages, are exhaustive and unique, ensuring no overlap between types.

// Handling these types necessitates a switch statement, covering all possible variants for completeness:
let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};

// For pattern matching, especially when not all cases are addressed explicitly, the wildcard &quot;_&quot; can be a fallback. The &quot;when&quot; keyword allows for additional conditions in matches, offering a concise way to handle complex patterns:
let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};

// Testing different cases to demonstrate how these functions work with the defined types:
let a = toMut(A); toString(a); a.value = change(a); toString(a);
let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);

/* DATABASE STORAGE FOR DATA SCIENCE */

// Working with generic types and function handling is one thing, but let&#x27;s step into a scenario where the stakes are higher: being data scientists at a medical center, tasked with deriving basic statistics from patient data. Given a raw database in a text file format, we&#x27;ve managed to extract key information as follows:

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];

// The data&#x27;s format is row-wise with an arbitrary order, which could include duplicates, missing, or extra items. To streamline debugging, we&#x27;re aiming to cast these to string maps.

// Here&#x27;s where the Map.Make functor comes into play, allowing us to generate a StringMap keyed by strings for easier readability and manipulation, akin to handling JSON objects:
module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});

// Converting our map to a JSON-like string for debug-friendliness:
let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};

// Transitioning to a generic database format, our row-wise data gets a transformation. Here, we&#x27;re all about clarity and correctness:
let showJson = true;
let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);

// Accessing the elements becomes straightforward. Missing elements? No biggie, we handle that gracefully:
let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};

// After some exploration and analysis, key insights emerge regarding age, weight, name, and gender. These form the cornerstone of our new database signature:
type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};

// Structuring a strictly-typed database while ensuring all necessary keys are included and defaults are set for missing items:
let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);

// Finally, the database is correctly formatted. Next up, transposing this database to a column-wise format, ready for statistical analysis:
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};

// Successfully transposing our data, we&#x27;re set to dive deep into the analysis, equipped with a database that&#x27;s both comprehensive and accurately structured.
let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));

/* STATISTICS LIBRARY DEVELOPMENT */

// Venturing into building a generic statistics library, we&#x27;re focusing on versatility across different data structures. Whether dealing with Lists or Arrays, the goal is seamless integration and handling.

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
  
// The challenge lies in unpacking these varied structures into a consistent format, ideally a list of primitives, for statistical analysis. Given the evolving nature of our library, not all types are fully supported yet, leading to potential exceptions for unhandled cases.
exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};

// To ensure a smooth user experience, we wrap secToList in a function that gracefully handles exceptions, providing clear feedback rather than abrupt errors.
let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};

// Diving into the core of our library, we aim to offer basic but essential statistical functions, each designed to work with a specific type of data.

// getCounts tackles enumeration, mapping each unique string in a list to its frequency of occurrence, ideal for categorical data analysis.
let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}

// getMedian finds the middle value in a list of floats after sorting, a key measure of central tendency for quantitative data.
let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};

// getMean computes the average from a list of floats, providing a quick snapshot of your data&#x27;s central value.
let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));

// Structuring our output, we define types for summarizing string and float data, encapsulating counts for categorical data and central measures for continuous data.
type stringStats = {
  counts: list((string, int)),
};

type floatStats = {
  mean: float,
  median: float,
};

/* DATA ANALYSIS FRAMEWORK */

// Integrating complex data structures into actionable insights requires a systematic approach. We&#x27;ve established methods to deconstruct complex data into primitive lists and have statistical functions ready. The challenge now is to seamlessly connect these components.

// First, let&#x27;s categorize data types based on their analytical utility:

// - Nominal data, like colors &quot;Blue&quot; and &quot;Yellow&quot;, are distinct without a meaningful order. The mode serves as their central tendency measure.
// - Boolean data, a subset of nominal, consists of binary choices like &quot;Yes&quot; and &quot;No&quot;.
// - Ordinal data, such as ratings from 1 (&quot;Low&quot;) to 5 (&quot;High&quot;), imply order but not the uniformity of scale. Their median reflects central tendency.
// - Numeric data, representing continuous or interval data, can be fully quantified. The mean is used to express their central tendency.

// Recognizing that not all operations apply universally across data types underscores the importance of targeted analytical strategies.

// Transitioning to the implementation phase:

// The `listToFloat` function converts a list of primitives to floats, selectively allowing boolean and integer conversions based on flags:
let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};

// Converting primitives to strings while handling incompatible types by casting to floats, then stringifying, allows for flexible data interpretation:
exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};

// `getFloatStats` and `getStringStats` functions then process these lists into statistical summaries, considering the data level restrictions and debug options respectively:
let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}

// Finally, transforming primitive lists to the expected input format for statistical analysis:
let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));

// Extracting statistics becomes straightforward with prepped data:
let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);

// Now, it&#x27;s just a matter of calling the appropriate statistical function for each data type, with optional debugging for string conversions:
getStringStats(names, ~debug=true, ());
getFloatStats(weights, ~level=1, ());
getStringStats(weights, ~debug=true, ());

getFloatStats(ages, ~level=2, ());
getStringStats(ages, ~debug=true, ());

getFloatStats(males, ~level=3, ());
getStringStats(males, ~debug=true, ());

db1.re

type mut(&#x27;a) = {
  mutable value: &#x27;a,
};
// type mut(&#x27;a) = { mutable value: &#x27;a, };

db10.re

let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};
// let mapToJson: StringMap.t(prim) =&gt; string = &lt;fun&gt;;

db11.re

let showJson = true;
// let showJson: bool = true;

let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);
/* let dbGeneric: list(StringMap.t(prim)) =
  [&lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;];
*/
/*
{age: +18, male: false, name: Ada, weight: +98.5}
{age: +25, male: true, name: Ben, weight: +81.5}
{age: +45, alive: true, name: Caz, weight: +70.6}
{age: +10, male: true, name: Dan, weight: +98.5}
{male: false, name: Eve}
*/

db12.re

let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};
// let tryAccessDbGeneric: (StringMap.key, int) =&gt; prim = &lt;fun&gt;;

db13.re

type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};
// type signature = { age: prim, weight: prim, name: prim, male: prim, };

db14.re

let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);
/*
let db: list(signature) =
  [{age: D(18), weight: E(98.5), name: F(&quot;Ada&quot;), male: B(false)},
   {age: D(25), weight: E(81.5), name: F(&quot;Ben&quot;), male: B(true)},
   {age: D(45), weight: E(70.6), name: F(&quot;Caz&quot;), male: A},
   {age: D(10), weight: E(98.5), name: F(&quot;Dan&quot;), male: B(true)},
   {age: A, weight: A, name: F(&quot;Eve&quot;), male: B(false)}];
*/

db15.re

type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
/*
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
*/

db16.re

let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));
/*
let dbCol: signatureColWise =
  {ageList: [D(18), D(25), D(45), D(10), A],
   weightList: [E(98.5), E(81.5), E(70.6), E(98.5), A],
   nameList: [F(&quot;Ada&quot;), F(&quot;Ben&quot;), F(&quot;Caz&quot;), F(&quot;Dan&quot;), F(&quot;Eve&quot;)],
   maleList: [B(false), B(true), A, B(true), B(false)]};
*/

db17.re

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
/* 
type sec =
    G(prim)
  | H(list(sec))
  | I(array(sec))
  | J((string, sec))
  | K({ key: string, value: sec, });
*/

db18.re

exception Unimplemented_type(string);
// exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};
// let secToList: sec =&gt; list(prim) = &lt;fun&gt;;

db19.re

let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};
// let trySecToList: sec =&gt; list(prim) = &lt;fun&gt;;

db2.re

let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
// let toMut: &#x27;a =&gt; mut(&#x27;a) = &lt;fun&gt;;

let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;
// let fromMut: mut(&#x27;a) =&gt; &#x27;a = &lt;fun&gt;;

db20.re

let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}
// let getCounts: list(StringMap.key) =&gt; list((string, int)) = &lt;fun&gt;;

db21.re

let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};
// let getMedian: list(float) =&gt; float = &lt;fun&gt;;

db22.re

let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));
// let getMean: list(float) =&gt; float = &lt;fun&gt;;

db23.re

type stringStats = {
  counts: list((string, int)),
};
// type stringStats = { counts: list((string, int)), };

type floatStats = {
  mean: float,
  median: float,
};
// type floatStats = { mean: float, median: float, };

db24.re

let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};
/*
let listToFloat:
  (list(prim), ~boolAllowed: bool=?, ~intAllowed: bool=?, unit) =&gt; list(float) =
  &lt;fun&gt;;
*/

db25.re

exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};
// let listToString: (list(prim), ~debug: bool=?, unit) =&gt; list(string) = &lt;fun&gt;;

db26.re

let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};
// let getFloatStats: (sec, ~level: int=?, unit) =&gt; floatStats = &lt;fun&gt;;

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}
// let getStringStats: (sec, ~debug: bool=?, unit) =&gt; stringStats = &lt;fun&gt;;

db27.re

let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));
// let primListToSec: list(prim) =&gt; sec = &lt;fun&gt;;

db28.re

let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);
/*
let ages: sec = H([G((D(18))), G((D(25))), G((D(45))), G((D(10))), G(A)]);
let weights: sec =
  H([G((E(98.5))), G((E(81.5))), G((E(70.6))), G((E(98.5))), G(A)]);
let names: sec =
  H([G((F(&quot;Ada&quot;))), G((F(&quot;Ben&quot;))), G((F(&quot;Caz&quot;))), G((F(&quot;Dan&quot;))), G((F(&quot;Eve&quot;)))]);
let males: sec =
  H([G((B(false))), G((B(true))), G(A), G((B(true))), G((B(false)))]);
*/

db29.re

getStringStats(names, ~debug=true, ());
// - : stringStats = {counts: [(&quot;Ada&quot;, 1), (&quot;Ben&quot;, 1), (&quot;Caz&quot;, 1), (&quot;Dan&quot;, 1), (&quot;Eve&quot;, 1)]}

getFloatStats(weights, ~level=1, ());
// - : floatStats = {mean: 87.275, median: 90.}

getStringStats(weights, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;70.6&quot;, 1), (&quot;81.5&quot;, 1), (&quot;98.5&quot;, 2)]}

getFloatStats(ages, ~level=2, ());
// - : floatStats = {mean: 24.5, median: 21.5}

getStringStats(ages, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;10.&quot;, 1), (&quot;18.&quot;, 1), (&quot;25.&quot;, 1), (&quot;45.&quot;, 1)]}

getFloatStats(males, ~level=3, ());
// - : floatStats = {mean: 0.5, median: 0.5}

getStringStats(males, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;0.&quot;, 2), (&quot;1.&quot;, 2)]}

db3.re

let x = ref(0); // Equivalent to let x = toMut(0);
// let x: ref(int) = {contents: 0};

x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);
// - : int = 1

db4.re

type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);
// type prim = A | B(bool) | C(char) | D(int) | E(float) | F(string);

db5.re

let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};
// let change: mut(prim) =&gt; prim = &lt;fun&gt;;

db6.re

let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};
// let toString: mut(prim) =&gt; string = &lt;fun&gt;;

db7.re

let a = toMut(A); toString(a); a.value = change(a); toString(a);
// let a: mut(prim) = {value: A};
// - : string = &quot;empty&quot;
// - : string = &quot;empty&quot;

let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
// let b: mut(prim) = {value: B(false)};
// - : string = &quot;false&quot;
// - : string = &quot;true&quot;

let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
// let c: mut(prim) = {value: C(&#x27;a&#x27;)};
// - : string = &quot;a&quot;
// - : string = &quot;b&quot;

let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
// let d: mut(prim) = {value: D(0)};
// - : string = &quot;0&quot;
// - : string = &quot;+1&quot;

let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
// let e: mut(prim) = {value: E(0.)};
// - : string = &quot;0.&quot;
// - : string = &quot;+1.&quot;

let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);
// let f: mut(prim) = {value: F(&quot;Hello&quot;)};
// - : string = &quot;Hello&quot;
// - : string = &quot;Hello!&quot;

db8.re

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];
/*
let dbRaw: list(array((string, prim))) =
  [[|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(false))|],
   [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)),
     (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)),
     (&quot;alive&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|]];

*/

db9.re

module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});
// module StringMap: { ... };</code></pre><p>To ensure a smooth user experience, we wrap secToList in a function that gracefully handles exceptions, providing clear feedback rather than abrupt errors.</p><pre><code>db.re

/* HANDLING PRIMITIVE TYPES */

// Mutability in ReasonML is a feature primarily used with records. Here&#x27;s how you define a mutable type that can hold any value:
type mut(&#x27;a) = {
  mutable value: &#x27;a,
};

// In λ-calculus, function types like f: A -&gt; B imply a transformation or proof from A to B. The functions toMut and fromMut serve as bridges between mutable and immutable types, showing they can be interchangeable:
let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;

// Using the standard implementation as a reference, you can see how it translates in practical terms:
let x = ref(0); // Equivalent to let x = toMut(0);
x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);

// ReasonML requires explicit type declarations for union types, unlike TypeScript where you might use &quot;int | null&quot;:
type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);

// Variant types in ReasonML, akin to sum types or dependent types in other languages, are exhaustive and unique, ensuring no overlap between types.

// Handling these types necessitates a switch statement, covering all possible variants for completeness:
let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};

// For pattern matching, especially when not all cases are addressed explicitly, the wildcard &quot;_&quot; can be a fallback. The &quot;when&quot; keyword allows for additional conditions in matches, offering a concise way to handle complex patterns:
let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};

// Testing different cases to demonstrate how these functions work with the defined types:
let a = toMut(A); toString(a); a.value = change(a); toString(a);
let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);

/* DATABASE STORAGE FOR DATA SCIENCE */

// Working with generic types and function handling is one thing, but let&#x27;s step into a scenario where the stakes are higher: being data scientists at a medical center, tasked with deriving basic statistics from patient data. Given a raw database in a text file format, we&#x27;ve managed to extract key information as follows:

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];

// The data&#x27;s format is row-wise with an arbitrary order, which could include duplicates, missing, or extra items. To streamline debugging, we&#x27;re aiming to cast these to string maps.

// Here&#x27;s where the Map.Make functor comes into play, allowing us to generate a StringMap keyed by strings for easier readability and manipulation, akin to handling JSON objects:
module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});

// Converting our map to a JSON-like string for debug-friendliness:
let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};

// Transitioning to a generic database format, our row-wise data gets a transformation. Here, we&#x27;re all about clarity and correctness:
let showJson = true;
let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);

// Accessing the elements becomes straightforward. Missing elements? No biggie, we handle that gracefully:
let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};

// After some exploration and analysis, key insights emerge regarding age, weight, name, and gender. These form the cornerstone of our new database signature:
type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};

// Structuring a strictly-typed database while ensuring all necessary keys are included and defaults are set for missing items:
let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);

// Finally, the database is correctly formatted. Next up, transposing this database to a column-wise format, ready for statistical analysis:
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};

// Successfully transposing our data, we&#x27;re set to dive deep into the analysis, equipped with a database that&#x27;s both comprehensive and accurately structured.
let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));

/* STATISTICS LIBRARY DEVELOPMENT */

// Venturing into building a generic statistics library, we&#x27;re focusing on versatility across different data structures. Whether dealing with Lists or Arrays, the goal is seamless integration and handling.

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
  
// The challenge lies in unpacking these varied structures into a consistent format, ideally a list of primitives, for statistical analysis. Given the evolving nature of our library, not all types are fully supported yet, leading to potential exceptions for unhandled cases.
exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};

// To ensure a smooth user experience, we wrap secToList in a function that gracefully handles exceptions, providing clear feedback rather than abrupt errors.
let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};

// Diving into the core of our library, we aim to offer basic but essential statistical functions, each designed to work with a specific type of data.

// getCounts tackles enumeration, mapping each unique string in a list to its frequency of occurrence, ideal for categorical data analysis.
let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}

// getMedian finds the middle value in a list of floats after sorting, a key measure of central tendency for quantitative data.
let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};

// getMean computes the average from a list of floats, providing a quick snapshot of your data&#x27;s central value.
let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));

// Structuring our output, we define types for summarizing string and float data, encapsulating counts for categorical data and central measures for continuous data.
type stringStats = {
  counts: list((string, int)),
};

type floatStats = {
  mean: float,
  median: float,
};

/* DATA ANALYSIS FRAMEWORK */

// Integrating complex data structures into actionable insights requires a systematic approach. We&#x27;ve established methods to deconstruct complex data into primitive lists and have statistical functions ready. The challenge now is to seamlessly connect these components.

// First, let&#x27;s categorize data types based on their analytical utility:

// - Nominal data, like colors &quot;Blue&quot; and &quot;Yellow&quot;, are distinct without a meaningful order. The mode serves as their central tendency measure.
// - Boolean data, a subset of nominal, consists of binary choices like &quot;Yes&quot; and &quot;No&quot;.
// - Ordinal data, such as ratings from 1 (&quot;Low&quot;) to 5 (&quot;High&quot;), imply order but not the uniformity of scale. Their median reflects central tendency.
// - Numeric data, representing continuous or interval data, can be fully quantified. The mean is used to express their central tendency.

// Recognizing that not all operations apply universally across data types underscores the importance of targeted analytical strategies.

// Transitioning to the implementation phase:

// The `listToFloat` function converts a list of primitives to floats, selectively allowing boolean and integer conversions based on flags:
let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};

// Converting primitives to strings while handling incompatible types by casting to floats, then stringifying, allows for flexible data interpretation:
exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};

// `getFloatStats` and `getStringStats` functions then process these lists into statistical summaries, considering the data level restrictions and debug options respectively:
let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}

// Finally, transforming primitive lists to the expected input format for statistical analysis:
let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));

// Extracting statistics becomes straightforward with prepped data:
let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);

// Now, it&#x27;s just a matter of calling the appropriate statistical function for each data type, with optional debugging for string conversions:
getStringStats(names, ~debug=true, ());
getFloatStats(weights, ~level=1, ());
getStringStats(weights, ~debug=true, ());

getFloatStats(ages, ~level=2, ());
getStringStats(ages, ~debug=true, ());

getFloatStats(males, ~level=3, ());
getStringStats(males, ~debug=true, ());

db1.re

type mut(&#x27;a) = {
  mutable value: &#x27;a,
};
// type mut(&#x27;a) = { mutable value: &#x27;a, };

db10.re

let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};
// let mapToJson: StringMap.t(prim) =&gt; string = &lt;fun&gt;;

db11.re

let showJson = true;
// let showJson: bool = true;

let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);
/* let dbGeneric: list(StringMap.t(prim)) =
  [&lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;];
*/
/*
{age: +18, male: false, name: Ada, weight: +98.5}
{age: +25, male: true, name: Ben, weight: +81.5}
{age: +45, alive: true, name: Caz, weight: +70.6}
{age: +10, male: true, name: Dan, weight: +98.5}
{male: false, name: Eve}
*/

db12.re

let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};
// let tryAccessDbGeneric: (StringMap.key, int) =&gt; prim = &lt;fun&gt;;

db13.re

type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};
// type signature = { age: prim, weight: prim, name: prim, male: prim, };

db14.re

let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);
/*
let db: list(signature) =
  [{age: D(18), weight: E(98.5), name: F(&quot;Ada&quot;), male: B(false)},
   {age: D(25), weight: E(81.5), name: F(&quot;Ben&quot;), male: B(true)},
   {age: D(45), weight: E(70.6), name: F(&quot;Caz&quot;), male: A},
   {age: D(10), weight: E(98.5), name: F(&quot;Dan&quot;), male: B(true)},
   {age: A, weight: A, name: F(&quot;Eve&quot;), male: B(false)}];
*/

db15.re

type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
/*
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
*/

db16.re

let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));
/*
let dbCol: signatureColWise =
  {ageList: [D(18), D(25), D(45), D(10), A],
   weightList: [E(98.5), E(81.5), E(70.6), E(98.5), A],
   nameList: [F(&quot;Ada&quot;), F(&quot;Ben&quot;), F(&quot;Caz&quot;), F(&quot;Dan&quot;), F(&quot;Eve&quot;)],
   maleList: [B(false), B(true), A, B(true), B(false)]};
*/

db17.re

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
/* 
type sec =
    G(prim)
  | H(list(sec))
  | I(array(sec))
  | J((string, sec))
  | K({ key: string, value: sec, });
*/

db18.re

exception Unimplemented_type(string);
// exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};
// let secToList: sec =&gt; list(prim) = &lt;fun&gt;;

db19.re

let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};
// let trySecToList: sec =&gt; list(prim) = &lt;fun&gt;;

db2.re

let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
// let toMut: &#x27;a =&gt; mut(&#x27;a) = &lt;fun&gt;;

let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;
// let fromMut: mut(&#x27;a) =&gt; &#x27;a = &lt;fun&gt;;

db20.re

let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}
// let getCounts: list(StringMap.key) =&gt; list((string, int)) = &lt;fun&gt;;

db21.re

let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};
// let getMedian: list(float) =&gt; float = &lt;fun&gt;;

db22.re

let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));
// let getMean: list(float) =&gt; float = &lt;fun&gt;;

db23.re

type stringStats = {
  counts: list((string, int)),
};
// type stringStats = { counts: list((string, int)), };

type floatStats = {
  mean: float,
  median: float,
};
// type floatStats = { mean: float, median: float, };

db24.re

let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};
/*
let listToFloat:
  (list(prim), ~boolAllowed: bool=?, ~intAllowed: bool=?, unit) =&gt; list(float) =
  &lt;fun&gt;;
*/

db25.re

exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};
// let listToString: (list(prim), ~debug: bool=?, unit) =&gt; list(string) = &lt;fun&gt;;

db26.re

let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};
// let getFloatStats: (sec, ~level: int=?, unit) =&gt; floatStats = &lt;fun&gt;;

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}
// let getStringStats: (sec, ~debug: bool=?, unit) =&gt; stringStats = &lt;fun&gt;;

db27.re

let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));
// let primListToSec: list(prim) =&gt; sec = &lt;fun&gt;;

db28.re

let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);
/*
let ages: sec = H([G((D(18))), G((D(25))), G((D(45))), G((D(10))), G(A)]);
let weights: sec =
  H([G((E(98.5))), G((E(81.5))), G((E(70.6))), G((E(98.5))), G(A)]);
let names: sec =
  H([G((F(&quot;Ada&quot;))), G((F(&quot;Ben&quot;))), G((F(&quot;Caz&quot;))), G((F(&quot;Dan&quot;))), G((F(&quot;Eve&quot;)))]);
let males: sec =
  H([G((B(false))), G((B(true))), G(A), G((B(true))), G((B(false)))]);
*/

db29.re

getStringStats(names, ~debug=true, ());
// - : stringStats = {counts: [(&quot;Ada&quot;, 1), (&quot;Ben&quot;, 1), (&quot;Caz&quot;, 1), (&quot;Dan&quot;, 1), (&quot;Eve&quot;, 1)]}

getFloatStats(weights, ~level=1, ());
// - : floatStats = {mean: 87.275, median: 90.}

getStringStats(weights, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;70.6&quot;, 1), (&quot;81.5&quot;, 1), (&quot;98.5&quot;, 2)]}

getFloatStats(ages, ~level=2, ());
// - : floatStats = {mean: 24.5, median: 21.5}

getStringStats(ages, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;10.&quot;, 1), (&quot;18.&quot;, 1), (&quot;25.&quot;, 1), (&quot;45.&quot;, 1)]}

getFloatStats(males, ~level=3, ());
// - : floatStats = {mean: 0.5, median: 0.5}

getStringStats(males, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;0.&quot;, 2), (&quot;1.&quot;, 2)]}

db3.re

let x = ref(0); // Equivalent to let x = toMut(0);
// let x: ref(int) = {contents: 0};

x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);
// - : int = 1

db4.re

type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);
// type prim = A | B(bool) | C(char) | D(int) | E(float) | F(string);

db5.re

let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};
// let change: mut(prim) =&gt; prim = &lt;fun&gt;;

db6.re

let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};
// let toString: mut(prim) =&gt; string = &lt;fun&gt;;

db7.re

let a = toMut(A); toString(a); a.value = change(a); toString(a);
// let a: mut(prim) = {value: A};
// - : string = &quot;empty&quot;
// - : string = &quot;empty&quot;

let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
// let b: mut(prim) = {value: B(false)};
// - : string = &quot;false&quot;
// - : string = &quot;true&quot;

let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
// let c: mut(prim) = {value: C(&#x27;a&#x27;)};
// - : string = &quot;a&quot;
// - : string = &quot;b&quot;

let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
// let d: mut(prim) = {value: D(0)};
// - : string = &quot;0&quot;
// - : string = &quot;+1&quot;

let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
// let e: mut(prim) = {value: E(0.)};
// - : string = &quot;0.&quot;
// - : string = &quot;+1.&quot;

let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);
// let f: mut(prim) = {value: F(&quot;Hello&quot;)};
// - : string = &quot;Hello&quot;
// - : string = &quot;Hello!&quot;

db8.re

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];
/*
let dbRaw: list(array((string, prim))) =
  [[|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(false))|],
   [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)),
     (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)),
     (&quot;alive&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|]];

*/

db9.re

module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});
// module StringMap: { ... };</code></pre><p>Diving into the core of our library, we aim to offer basic but essential statistical functions, each designed to work with a specific type of data.</p><p>getCounts tackles enumeration, mapping each unique string in a list to its frequency of occurrence, ideal for categorical data analysis.</p><pre><code>db.re

/* HANDLING PRIMITIVE TYPES */

// Mutability in ReasonML is a feature primarily used with records. Here&#x27;s how you define a mutable type that can hold any value:
type mut(&#x27;a) = {
  mutable value: &#x27;a,
};

// In λ-calculus, function types like f: A -&gt; B imply a transformation or proof from A to B. The functions toMut and fromMut serve as bridges between mutable and immutable types, showing they can be interchangeable:
let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;

// Using the standard implementation as a reference, you can see how it translates in practical terms:
let x = ref(0); // Equivalent to let x = toMut(0);
x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);

// ReasonML requires explicit type declarations for union types, unlike TypeScript where you might use &quot;int | null&quot;:
type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);

// Variant types in ReasonML, akin to sum types or dependent types in other languages, are exhaustive and unique, ensuring no overlap between types.

// Handling these types necessitates a switch statement, covering all possible variants for completeness:
let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};

// For pattern matching, especially when not all cases are addressed explicitly, the wildcard &quot;_&quot; can be a fallback. The &quot;when&quot; keyword allows for additional conditions in matches, offering a concise way to handle complex patterns:
let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};

// Testing different cases to demonstrate how these functions work with the defined types:
let a = toMut(A); toString(a); a.value = change(a); toString(a);
let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);

/* DATABASE STORAGE FOR DATA SCIENCE */

// Working with generic types and function handling is one thing, but let&#x27;s step into a scenario where the stakes are higher: being data scientists at a medical center, tasked with deriving basic statistics from patient data. Given a raw database in a text file format, we&#x27;ve managed to extract key information as follows:

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];

// The data&#x27;s format is row-wise with an arbitrary order, which could include duplicates, missing, or extra items. To streamline debugging, we&#x27;re aiming to cast these to string maps.

// Here&#x27;s where the Map.Make functor comes into play, allowing us to generate a StringMap keyed by strings for easier readability and manipulation, akin to handling JSON objects:
module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});

// Converting our map to a JSON-like string for debug-friendliness:
let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};

// Transitioning to a generic database format, our row-wise data gets a transformation. Here, we&#x27;re all about clarity and correctness:
let showJson = true;
let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);

// Accessing the elements becomes straightforward. Missing elements? No biggie, we handle that gracefully:
let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};

// After some exploration and analysis, key insights emerge regarding age, weight, name, and gender. These form the cornerstone of our new database signature:
type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};

// Structuring a strictly-typed database while ensuring all necessary keys are included and defaults are set for missing items:
let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);

// Finally, the database is correctly formatted. Next up, transposing this database to a column-wise format, ready for statistical analysis:
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};

// Successfully transposing our data, we&#x27;re set to dive deep into the analysis, equipped with a database that&#x27;s both comprehensive and accurately structured.
let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));

/* STATISTICS LIBRARY DEVELOPMENT */

// Venturing into building a generic statistics library, we&#x27;re focusing on versatility across different data structures. Whether dealing with Lists or Arrays, the goal is seamless integration and handling.

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
  
// The challenge lies in unpacking these varied structures into a consistent format, ideally a list of primitives, for statistical analysis. Given the evolving nature of our library, not all types are fully supported yet, leading to potential exceptions for unhandled cases.
exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};

// To ensure a smooth user experience, we wrap secToList in a function that gracefully handles exceptions, providing clear feedback rather than abrupt errors.
let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};

// Diving into the core of our library, we aim to offer basic but essential statistical functions, each designed to work with a specific type of data.

// getCounts tackles enumeration, mapping each unique string in a list to its frequency of occurrence, ideal for categorical data analysis.
let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}

// getMedian finds the middle value in a list of floats after sorting, a key measure of central tendency for quantitative data.
let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};

// getMean computes the average from a list of floats, providing a quick snapshot of your data&#x27;s central value.
let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));

// Structuring our output, we define types for summarizing string and float data, encapsulating counts for categorical data and central measures for continuous data.
type stringStats = {
  counts: list((string, int)),
};

type floatStats = {
  mean: float,
  median: float,
};

/* DATA ANALYSIS FRAMEWORK */

// Integrating complex data structures into actionable insights requires a systematic approach. We&#x27;ve established methods to deconstruct complex data into primitive lists and have statistical functions ready. The challenge now is to seamlessly connect these components.

// First, let&#x27;s categorize data types based on their analytical utility:

// - Nominal data, like colors &quot;Blue&quot; and &quot;Yellow&quot;, are distinct without a meaningful order. The mode serves as their central tendency measure.
// - Boolean data, a subset of nominal, consists of binary choices like &quot;Yes&quot; and &quot;No&quot;.
// - Ordinal data, such as ratings from 1 (&quot;Low&quot;) to 5 (&quot;High&quot;), imply order but not the uniformity of scale. Their median reflects central tendency.
// - Numeric data, representing continuous or interval data, can be fully quantified. The mean is used to express their central tendency.

// Recognizing that not all operations apply universally across data types underscores the importance of targeted analytical strategies.

// Transitioning to the implementation phase:

// The `listToFloat` function converts a list of primitives to floats, selectively allowing boolean and integer conversions based on flags:
let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};

// Converting primitives to strings while handling incompatible types by casting to floats, then stringifying, allows for flexible data interpretation:
exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};

// `getFloatStats` and `getStringStats` functions then process these lists into statistical summaries, considering the data level restrictions and debug options respectively:
let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}

// Finally, transforming primitive lists to the expected input format for statistical analysis:
let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));

// Extracting statistics becomes straightforward with prepped data:
let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);

// Now, it&#x27;s just a matter of calling the appropriate statistical function for each data type, with optional debugging for string conversions:
getStringStats(names, ~debug=true, ());
getFloatStats(weights, ~level=1, ());
getStringStats(weights, ~debug=true, ());

getFloatStats(ages, ~level=2, ());
getStringStats(ages, ~debug=true, ());

getFloatStats(males, ~level=3, ());
getStringStats(males, ~debug=true, ());

db1.re

type mut(&#x27;a) = {
  mutable value: &#x27;a,
};
// type mut(&#x27;a) = { mutable value: &#x27;a, };

db10.re

let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};
// let mapToJson: StringMap.t(prim) =&gt; string = &lt;fun&gt;;

db11.re

let showJson = true;
// let showJson: bool = true;

let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);
/* let dbGeneric: list(StringMap.t(prim)) =
  [&lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;];
*/
/*
{age: +18, male: false, name: Ada, weight: +98.5}
{age: +25, male: true, name: Ben, weight: +81.5}
{age: +45, alive: true, name: Caz, weight: +70.6}
{age: +10, male: true, name: Dan, weight: +98.5}
{male: false, name: Eve}
*/

db12.re

let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};
// let tryAccessDbGeneric: (StringMap.key, int) =&gt; prim = &lt;fun&gt;;

db13.re

type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};
// type signature = { age: prim, weight: prim, name: prim, male: prim, };

db14.re

let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);
/*
let db: list(signature) =
  [{age: D(18), weight: E(98.5), name: F(&quot;Ada&quot;), male: B(false)},
   {age: D(25), weight: E(81.5), name: F(&quot;Ben&quot;), male: B(true)},
   {age: D(45), weight: E(70.6), name: F(&quot;Caz&quot;), male: A},
   {age: D(10), weight: E(98.5), name: F(&quot;Dan&quot;), male: B(true)},
   {age: A, weight: A, name: F(&quot;Eve&quot;), male: B(false)}];
*/

db15.re

type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
/*
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
*/

db16.re

let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));
/*
let dbCol: signatureColWise =
  {ageList: [D(18), D(25), D(45), D(10), A],
   weightList: [E(98.5), E(81.5), E(70.6), E(98.5), A],
   nameList: [F(&quot;Ada&quot;), F(&quot;Ben&quot;), F(&quot;Caz&quot;), F(&quot;Dan&quot;), F(&quot;Eve&quot;)],
   maleList: [B(false), B(true), A, B(true), B(false)]};
*/

db17.re

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
/* 
type sec =
    G(prim)
  | H(list(sec))
  | I(array(sec))
  | J((string, sec))
  | K({ key: string, value: sec, });
*/

db18.re

exception Unimplemented_type(string);
// exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};
// let secToList: sec =&gt; list(prim) = &lt;fun&gt;;

db19.re

let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};
// let trySecToList: sec =&gt; list(prim) = &lt;fun&gt;;

db2.re

let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
// let toMut: &#x27;a =&gt; mut(&#x27;a) = &lt;fun&gt;;

let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;
// let fromMut: mut(&#x27;a) =&gt; &#x27;a = &lt;fun&gt;;

db20.re

let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}
// let getCounts: list(StringMap.key) =&gt; list((string, int)) = &lt;fun&gt;;

db21.re

let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};
// let getMedian: list(float) =&gt; float = &lt;fun&gt;;

db22.re

let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));
// let getMean: list(float) =&gt; float = &lt;fun&gt;;

db23.re

type stringStats = {
  counts: list((string, int)),
};
// type stringStats = { counts: list((string, int)), };

type floatStats = {
  mean: float,
  median: float,
};
// type floatStats = { mean: float, median: float, };

db24.re

let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};
/*
let listToFloat:
  (list(prim), ~boolAllowed: bool=?, ~intAllowed: bool=?, unit) =&gt; list(float) =
  &lt;fun&gt;;
*/

db25.re

exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};
// let listToString: (list(prim), ~debug: bool=?, unit) =&gt; list(string) = &lt;fun&gt;;

db26.re

let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};
// let getFloatStats: (sec, ~level: int=?, unit) =&gt; floatStats = &lt;fun&gt;;

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}
// let getStringStats: (sec, ~debug: bool=?, unit) =&gt; stringStats = &lt;fun&gt;;

db27.re

let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));
// let primListToSec: list(prim) =&gt; sec = &lt;fun&gt;;

db28.re

let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);
/*
let ages: sec = H([G((D(18))), G((D(25))), G((D(45))), G((D(10))), G(A)]);
let weights: sec =
  H([G((E(98.5))), G((E(81.5))), G((E(70.6))), G((E(98.5))), G(A)]);
let names: sec =
  H([G((F(&quot;Ada&quot;))), G((F(&quot;Ben&quot;))), G((F(&quot;Caz&quot;))), G((F(&quot;Dan&quot;))), G((F(&quot;Eve&quot;)))]);
let males: sec =
  H([G((B(false))), G((B(true))), G(A), G((B(true))), G((B(false)))]);
*/

db29.re

getStringStats(names, ~debug=true, ());
// - : stringStats = {counts: [(&quot;Ada&quot;, 1), (&quot;Ben&quot;, 1), (&quot;Caz&quot;, 1), (&quot;Dan&quot;, 1), (&quot;Eve&quot;, 1)]}

getFloatStats(weights, ~level=1, ());
// - : floatStats = {mean: 87.275, median: 90.}

getStringStats(weights, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;70.6&quot;, 1), (&quot;81.5&quot;, 1), (&quot;98.5&quot;, 2)]}

getFloatStats(ages, ~level=2, ());
// - : floatStats = {mean: 24.5, median: 21.5}

getStringStats(ages, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;10.&quot;, 1), (&quot;18.&quot;, 1), (&quot;25.&quot;, 1), (&quot;45.&quot;, 1)]}

getFloatStats(males, ~level=3, ());
// - : floatStats = {mean: 0.5, median: 0.5}

getStringStats(males, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;0.&quot;, 2), (&quot;1.&quot;, 2)]}

db3.re

let x = ref(0); // Equivalent to let x = toMut(0);
// let x: ref(int) = {contents: 0};

x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);
// - : int = 1

db4.re

type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);
// type prim = A | B(bool) | C(char) | D(int) | E(float) | F(string);

db5.re

let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};
// let change: mut(prim) =&gt; prim = &lt;fun&gt;;

db6.re

let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};
// let toString: mut(prim) =&gt; string = &lt;fun&gt;;

db7.re

let a = toMut(A); toString(a); a.value = change(a); toString(a);
// let a: mut(prim) = {value: A};
// - : string = &quot;empty&quot;
// - : string = &quot;empty&quot;

let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
// let b: mut(prim) = {value: B(false)};
// - : string = &quot;false&quot;
// - : string = &quot;true&quot;

let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
// let c: mut(prim) = {value: C(&#x27;a&#x27;)};
// - : string = &quot;a&quot;
// - : string = &quot;b&quot;

let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
// let d: mut(prim) = {value: D(0)};
// - : string = &quot;0&quot;
// - : string = &quot;+1&quot;

let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
// let e: mut(prim) = {value: E(0.)};
// - : string = &quot;0.&quot;
// - : string = &quot;+1.&quot;

let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);
// let f: mut(prim) = {value: F(&quot;Hello&quot;)};
// - : string = &quot;Hello&quot;
// - : string = &quot;Hello!&quot;

db8.re

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];
/*
let dbRaw: list(array((string, prim))) =
  [[|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(false))|],
   [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)),
     (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)),
     (&quot;alive&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|]];

*/

db9.re

module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});
// module StringMap: { ... };</code></pre><p>getMedian finds the middle value in a list of floats after sorting, a key measure of central tendency for quantitative data.</p><pre><code>db.re

/* HANDLING PRIMITIVE TYPES */

// Mutability in ReasonML is a feature primarily used with records. Here&#x27;s how you define a mutable type that can hold any value:
type mut(&#x27;a) = {
  mutable value: &#x27;a,
};

// In λ-calculus, function types like f: A -&gt; B imply a transformation or proof from A to B. The functions toMut and fromMut serve as bridges between mutable and immutable types, showing they can be interchangeable:
let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;

// Using the standard implementation as a reference, you can see how it translates in practical terms:
let x = ref(0); // Equivalent to let x = toMut(0);
x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);

// ReasonML requires explicit type declarations for union types, unlike TypeScript where you might use &quot;int | null&quot;:
type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);

// Variant types in ReasonML, akin to sum types or dependent types in other languages, are exhaustive and unique, ensuring no overlap between types.

// Handling these types necessitates a switch statement, covering all possible variants for completeness:
let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};

// For pattern matching, especially when not all cases are addressed explicitly, the wildcard &quot;_&quot; can be a fallback. The &quot;when&quot; keyword allows for additional conditions in matches, offering a concise way to handle complex patterns:
let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};

// Testing different cases to demonstrate how these functions work with the defined types:
let a = toMut(A); toString(a); a.value = change(a); toString(a);
let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);

/* DATABASE STORAGE FOR DATA SCIENCE */

// Working with generic types and function handling is one thing, but let&#x27;s step into a scenario where the stakes are higher: being data scientists at a medical center, tasked with deriving basic statistics from patient data. Given a raw database in a text file format, we&#x27;ve managed to extract key information as follows:

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];

// The data&#x27;s format is row-wise with an arbitrary order, which could include duplicates, missing, or extra items. To streamline debugging, we&#x27;re aiming to cast these to string maps.

// Here&#x27;s where the Map.Make functor comes into play, allowing us to generate a StringMap keyed by strings for easier readability and manipulation, akin to handling JSON objects:
module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});

// Converting our map to a JSON-like string for debug-friendliness:
let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};

// Transitioning to a generic database format, our row-wise data gets a transformation. Here, we&#x27;re all about clarity and correctness:
let showJson = true;
let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);

// Accessing the elements becomes straightforward. Missing elements? No biggie, we handle that gracefully:
let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};

// After some exploration and analysis, key insights emerge regarding age, weight, name, and gender. These form the cornerstone of our new database signature:
type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};

// Structuring a strictly-typed database while ensuring all necessary keys are included and defaults are set for missing items:
let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);

// Finally, the database is correctly formatted. Next up, transposing this database to a column-wise format, ready for statistical analysis:
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};

// Successfully transposing our data, we&#x27;re set to dive deep into the analysis, equipped with a database that&#x27;s both comprehensive and accurately structured.
let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));

/* STATISTICS LIBRARY DEVELOPMENT */

// Venturing into building a generic statistics library, we&#x27;re focusing on versatility across different data structures. Whether dealing with Lists or Arrays, the goal is seamless integration and handling.

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
  
// The challenge lies in unpacking these varied structures into a consistent format, ideally a list of primitives, for statistical analysis. Given the evolving nature of our library, not all types are fully supported yet, leading to potential exceptions for unhandled cases.
exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};

// To ensure a smooth user experience, we wrap secToList in a function that gracefully handles exceptions, providing clear feedback rather than abrupt errors.
let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};

// Diving into the core of our library, we aim to offer basic but essential statistical functions, each designed to work with a specific type of data.

// getCounts tackles enumeration, mapping each unique string in a list to its frequency of occurrence, ideal for categorical data analysis.
let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}

// getMedian finds the middle value in a list of floats after sorting, a key measure of central tendency for quantitative data.
let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};

// getMean computes the average from a list of floats, providing a quick snapshot of your data&#x27;s central value.
let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));

// Structuring our output, we define types for summarizing string and float data, encapsulating counts for categorical data and central measures for continuous data.
type stringStats = {
  counts: list((string, int)),
};

type floatStats = {
  mean: float,
  median: float,
};

/* DATA ANALYSIS FRAMEWORK */

// Integrating complex data structures into actionable insights requires a systematic approach. We&#x27;ve established methods to deconstruct complex data into primitive lists and have statistical functions ready. The challenge now is to seamlessly connect these components.

// First, let&#x27;s categorize data types based on their analytical utility:

// - Nominal data, like colors &quot;Blue&quot; and &quot;Yellow&quot;, are distinct without a meaningful order. The mode serves as their central tendency measure.
// - Boolean data, a subset of nominal, consists of binary choices like &quot;Yes&quot; and &quot;No&quot;.
// - Ordinal data, such as ratings from 1 (&quot;Low&quot;) to 5 (&quot;High&quot;), imply order but not the uniformity of scale. Their median reflects central tendency.
// - Numeric data, representing continuous or interval data, can be fully quantified. The mean is used to express their central tendency.

// Recognizing that not all operations apply universally across data types underscores the importance of targeted analytical strategies.

// Transitioning to the implementation phase:

// The `listToFloat` function converts a list of primitives to floats, selectively allowing boolean and integer conversions based on flags:
let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};

// Converting primitives to strings while handling incompatible types by casting to floats, then stringifying, allows for flexible data interpretation:
exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};

// `getFloatStats` and `getStringStats` functions then process these lists into statistical summaries, considering the data level restrictions and debug options respectively:
let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}

// Finally, transforming primitive lists to the expected input format for statistical analysis:
let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));

// Extracting statistics becomes straightforward with prepped data:
let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);

// Now, it&#x27;s just a matter of calling the appropriate statistical function for each data type, with optional debugging for string conversions:
getStringStats(names, ~debug=true, ());
getFloatStats(weights, ~level=1, ());
getStringStats(weights, ~debug=true, ());

getFloatStats(ages, ~level=2, ());
getStringStats(ages, ~debug=true, ());

getFloatStats(males, ~level=3, ());
getStringStats(males, ~debug=true, ());

db1.re

type mut(&#x27;a) = {
  mutable value: &#x27;a,
};
// type mut(&#x27;a) = { mutable value: &#x27;a, };

db10.re

let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};
// let mapToJson: StringMap.t(prim) =&gt; string = &lt;fun&gt;;

db11.re

let showJson = true;
// let showJson: bool = true;

let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);
/* let dbGeneric: list(StringMap.t(prim)) =
  [&lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;];
*/
/*
{age: +18, male: false, name: Ada, weight: +98.5}
{age: +25, male: true, name: Ben, weight: +81.5}
{age: +45, alive: true, name: Caz, weight: +70.6}
{age: +10, male: true, name: Dan, weight: +98.5}
{male: false, name: Eve}
*/

db12.re

let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};
// let tryAccessDbGeneric: (StringMap.key, int) =&gt; prim = &lt;fun&gt;;

db13.re

type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};
// type signature = { age: prim, weight: prim, name: prim, male: prim, };

db14.re

let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);
/*
let db: list(signature) =
  [{age: D(18), weight: E(98.5), name: F(&quot;Ada&quot;), male: B(false)},
   {age: D(25), weight: E(81.5), name: F(&quot;Ben&quot;), male: B(true)},
   {age: D(45), weight: E(70.6), name: F(&quot;Caz&quot;), male: A},
   {age: D(10), weight: E(98.5), name: F(&quot;Dan&quot;), male: B(true)},
   {age: A, weight: A, name: F(&quot;Eve&quot;), male: B(false)}];
*/

db15.re

type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
/*
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
*/

db16.re

let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));
/*
let dbCol: signatureColWise =
  {ageList: [D(18), D(25), D(45), D(10), A],
   weightList: [E(98.5), E(81.5), E(70.6), E(98.5), A],
   nameList: [F(&quot;Ada&quot;), F(&quot;Ben&quot;), F(&quot;Caz&quot;), F(&quot;Dan&quot;), F(&quot;Eve&quot;)],
   maleList: [B(false), B(true), A, B(true), B(false)]};
*/

db17.re

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
/* 
type sec =
    G(prim)
  | H(list(sec))
  | I(array(sec))
  | J((string, sec))
  | K({ key: string, value: sec, });
*/

db18.re

exception Unimplemented_type(string);
// exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};
// let secToList: sec =&gt; list(prim) = &lt;fun&gt;;

db19.re

let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};
// let trySecToList: sec =&gt; list(prim) = &lt;fun&gt;;

db2.re

let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
// let toMut: &#x27;a =&gt; mut(&#x27;a) = &lt;fun&gt;;

let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;
// let fromMut: mut(&#x27;a) =&gt; &#x27;a = &lt;fun&gt;;

db20.re

let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}
// let getCounts: list(StringMap.key) =&gt; list((string, int)) = &lt;fun&gt;;

db21.re

let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};
// let getMedian: list(float) =&gt; float = &lt;fun&gt;;

db22.re

let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));
// let getMean: list(float) =&gt; float = &lt;fun&gt;;

db23.re

type stringStats = {
  counts: list((string, int)),
};
// type stringStats = { counts: list((string, int)), };

type floatStats = {
  mean: float,
  median: float,
};
// type floatStats = { mean: float, median: float, };

db24.re

let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};
/*
let listToFloat:
  (list(prim), ~boolAllowed: bool=?, ~intAllowed: bool=?, unit) =&gt; list(float) =
  &lt;fun&gt;;
*/

db25.re

exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};
// let listToString: (list(prim), ~debug: bool=?, unit) =&gt; list(string) = &lt;fun&gt;;

db26.re

let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};
// let getFloatStats: (sec, ~level: int=?, unit) =&gt; floatStats = &lt;fun&gt;;

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}
// let getStringStats: (sec, ~debug: bool=?, unit) =&gt; stringStats = &lt;fun&gt;;

db27.re

let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));
// let primListToSec: list(prim) =&gt; sec = &lt;fun&gt;;

db28.re

let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);
/*
let ages: sec = H([G((D(18))), G((D(25))), G((D(45))), G((D(10))), G(A)]);
let weights: sec =
  H([G((E(98.5))), G((E(81.5))), G((E(70.6))), G((E(98.5))), G(A)]);
let names: sec =
  H([G((F(&quot;Ada&quot;))), G((F(&quot;Ben&quot;))), G((F(&quot;Caz&quot;))), G((F(&quot;Dan&quot;))), G((F(&quot;Eve&quot;)))]);
let males: sec =
  H([G((B(false))), G((B(true))), G(A), G((B(true))), G((B(false)))]);
*/

db29.re

getStringStats(names, ~debug=true, ());
// - : stringStats = {counts: [(&quot;Ada&quot;, 1), (&quot;Ben&quot;, 1), (&quot;Caz&quot;, 1), (&quot;Dan&quot;, 1), (&quot;Eve&quot;, 1)]}

getFloatStats(weights, ~level=1, ());
// - : floatStats = {mean: 87.275, median: 90.}

getStringStats(weights, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;70.6&quot;, 1), (&quot;81.5&quot;, 1), (&quot;98.5&quot;, 2)]}

getFloatStats(ages, ~level=2, ());
// - : floatStats = {mean: 24.5, median: 21.5}

getStringStats(ages, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;10.&quot;, 1), (&quot;18.&quot;, 1), (&quot;25.&quot;, 1), (&quot;45.&quot;, 1)]}

getFloatStats(males, ~level=3, ());
// - : floatStats = {mean: 0.5, median: 0.5}

getStringStats(males, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;0.&quot;, 2), (&quot;1.&quot;, 2)]}

db3.re

let x = ref(0); // Equivalent to let x = toMut(0);
// let x: ref(int) = {contents: 0};

x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);
// - : int = 1

db4.re

type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);
// type prim = A | B(bool) | C(char) | D(int) | E(float) | F(string);

db5.re

let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};
// let change: mut(prim) =&gt; prim = &lt;fun&gt;;

db6.re

let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};
// let toString: mut(prim) =&gt; string = &lt;fun&gt;;

db7.re

let a = toMut(A); toString(a); a.value = change(a); toString(a);
// let a: mut(prim) = {value: A};
// - : string = &quot;empty&quot;
// - : string = &quot;empty&quot;

let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
// let b: mut(prim) = {value: B(false)};
// - : string = &quot;false&quot;
// - : string = &quot;true&quot;

let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
// let c: mut(prim) = {value: C(&#x27;a&#x27;)};
// - : string = &quot;a&quot;
// - : string = &quot;b&quot;

let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
// let d: mut(prim) = {value: D(0)};
// - : string = &quot;0&quot;
// - : string = &quot;+1&quot;

let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
// let e: mut(prim) = {value: E(0.)};
// - : string = &quot;0.&quot;
// - : string = &quot;+1.&quot;

let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);
// let f: mut(prim) = {value: F(&quot;Hello&quot;)};
// - : string = &quot;Hello&quot;
// - : string = &quot;Hello!&quot;

db8.re

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];
/*
let dbRaw: list(array((string, prim))) =
  [[|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(false))|],
   [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)),
     (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)),
     (&quot;alive&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|]];

*/

db9.re

module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});
// module StringMap: { ... };</code></pre><p>getMean computes the average from a list of floats, providing a quick snapshot of your data’s central value.</p><pre><code>db.re

/* HANDLING PRIMITIVE TYPES */

// Mutability in ReasonML is a feature primarily used with records. Here&#x27;s how you define a mutable type that can hold any value:
type mut(&#x27;a) = {
  mutable value: &#x27;a,
};

// In λ-calculus, function types like f: A -&gt; B imply a transformation or proof from A to B. The functions toMut and fromMut serve as bridges between mutable and immutable types, showing they can be interchangeable:
let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;

// Using the standard implementation as a reference, you can see how it translates in practical terms:
let x = ref(0); // Equivalent to let x = toMut(0);
x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);

// ReasonML requires explicit type declarations for union types, unlike TypeScript where you might use &quot;int | null&quot;:
type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);

// Variant types in ReasonML, akin to sum types or dependent types in other languages, are exhaustive and unique, ensuring no overlap between types.

// Handling these types necessitates a switch statement, covering all possible variants for completeness:
let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};

// For pattern matching, especially when not all cases are addressed explicitly, the wildcard &quot;_&quot; can be a fallback. The &quot;when&quot; keyword allows for additional conditions in matches, offering a concise way to handle complex patterns:
let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};

// Testing different cases to demonstrate how these functions work with the defined types:
let a = toMut(A); toString(a); a.value = change(a); toString(a);
let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);

/* DATABASE STORAGE FOR DATA SCIENCE */

// Working with generic types and function handling is one thing, but let&#x27;s step into a scenario where the stakes are higher: being data scientists at a medical center, tasked with deriving basic statistics from patient data. Given a raw database in a text file format, we&#x27;ve managed to extract key information as follows:

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];

// The data&#x27;s format is row-wise with an arbitrary order, which could include duplicates, missing, or extra items. To streamline debugging, we&#x27;re aiming to cast these to string maps.

// Here&#x27;s where the Map.Make functor comes into play, allowing us to generate a StringMap keyed by strings for easier readability and manipulation, akin to handling JSON objects:
module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});

// Converting our map to a JSON-like string for debug-friendliness:
let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};

// Transitioning to a generic database format, our row-wise data gets a transformation. Here, we&#x27;re all about clarity and correctness:
let showJson = true;
let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);

// Accessing the elements becomes straightforward. Missing elements? No biggie, we handle that gracefully:
let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};

// After some exploration and analysis, key insights emerge regarding age, weight, name, and gender. These form the cornerstone of our new database signature:
type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};

// Structuring a strictly-typed database while ensuring all necessary keys are included and defaults are set for missing items:
let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);

// Finally, the database is correctly formatted. Next up, transposing this database to a column-wise format, ready for statistical analysis:
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};

// Successfully transposing our data, we&#x27;re set to dive deep into the analysis, equipped with a database that&#x27;s both comprehensive and accurately structured.
let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));

/* STATISTICS LIBRARY DEVELOPMENT */

// Venturing into building a generic statistics library, we&#x27;re focusing on versatility across different data structures. Whether dealing with Lists or Arrays, the goal is seamless integration and handling.

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
  
// The challenge lies in unpacking these varied structures into a consistent format, ideally a list of primitives, for statistical analysis. Given the evolving nature of our library, not all types are fully supported yet, leading to potential exceptions for unhandled cases.
exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};

// To ensure a smooth user experience, we wrap secToList in a function that gracefully handles exceptions, providing clear feedback rather than abrupt errors.
let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};

// Diving into the core of our library, we aim to offer basic but essential statistical functions, each designed to work with a specific type of data.

// getCounts tackles enumeration, mapping each unique string in a list to its frequency of occurrence, ideal for categorical data analysis.
let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}

// getMedian finds the middle value in a list of floats after sorting, a key measure of central tendency for quantitative data.
let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};

// getMean computes the average from a list of floats, providing a quick snapshot of your data&#x27;s central value.
let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));

// Structuring our output, we define types for summarizing string and float data, encapsulating counts for categorical data and central measures for continuous data.
type stringStats = {
  counts: list((string, int)),
};

type floatStats = {
  mean: float,
  median: float,
};

/* DATA ANALYSIS FRAMEWORK */

// Integrating complex data structures into actionable insights requires a systematic approach. We&#x27;ve established methods to deconstruct complex data into primitive lists and have statistical functions ready. The challenge now is to seamlessly connect these components.

// First, let&#x27;s categorize data types based on their analytical utility:

// - Nominal data, like colors &quot;Blue&quot; and &quot;Yellow&quot;, are distinct without a meaningful order. The mode serves as their central tendency measure.
// - Boolean data, a subset of nominal, consists of binary choices like &quot;Yes&quot; and &quot;No&quot;.
// - Ordinal data, such as ratings from 1 (&quot;Low&quot;) to 5 (&quot;High&quot;), imply order but not the uniformity of scale. Their median reflects central tendency.
// - Numeric data, representing continuous or interval data, can be fully quantified. The mean is used to express their central tendency.

// Recognizing that not all operations apply universally across data types underscores the importance of targeted analytical strategies.

// Transitioning to the implementation phase:

// The `listToFloat` function converts a list of primitives to floats, selectively allowing boolean and integer conversions based on flags:
let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};

// Converting primitives to strings while handling incompatible types by casting to floats, then stringifying, allows for flexible data interpretation:
exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};

// `getFloatStats` and `getStringStats` functions then process these lists into statistical summaries, considering the data level restrictions and debug options respectively:
let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}

// Finally, transforming primitive lists to the expected input format for statistical analysis:
let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));

// Extracting statistics becomes straightforward with prepped data:
let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);

// Now, it&#x27;s just a matter of calling the appropriate statistical function for each data type, with optional debugging for string conversions:
getStringStats(names, ~debug=true, ());
getFloatStats(weights, ~level=1, ());
getStringStats(weights, ~debug=true, ());

getFloatStats(ages, ~level=2, ());
getStringStats(ages, ~debug=true, ());

getFloatStats(males, ~level=3, ());
getStringStats(males, ~debug=true, ());

db1.re

type mut(&#x27;a) = {
  mutable value: &#x27;a,
};
// type mut(&#x27;a) = { mutable value: &#x27;a, };

db10.re

let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};
// let mapToJson: StringMap.t(prim) =&gt; string = &lt;fun&gt;;

db11.re

let showJson = true;
// let showJson: bool = true;

let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);
/* let dbGeneric: list(StringMap.t(prim)) =
  [&lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;];
*/
/*
{age: +18, male: false, name: Ada, weight: +98.5}
{age: +25, male: true, name: Ben, weight: +81.5}
{age: +45, alive: true, name: Caz, weight: +70.6}
{age: +10, male: true, name: Dan, weight: +98.5}
{male: false, name: Eve}
*/

db12.re

let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};
// let tryAccessDbGeneric: (StringMap.key, int) =&gt; prim = &lt;fun&gt;;

db13.re

type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};
// type signature = { age: prim, weight: prim, name: prim, male: prim, };

db14.re

let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);
/*
let db: list(signature) =
  [{age: D(18), weight: E(98.5), name: F(&quot;Ada&quot;), male: B(false)},
   {age: D(25), weight: E(81.5), name: F(&quot;Ben&quot;), male: B(true)},
   {age: D(45), weight: E(70.6), name: F(&quot;Caz&quot;), male: A},
   {age: D(10), weight: E(98.5), name: F(&quot;Dan&quot;), male: B(true)},
   {age: A, weight: A, name: F(&quot;Eve&quot;), male: B(false)}];
*/

db15.re

type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
/*
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
*/

db16.re

let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));
/*
let dbCol: signatureColWise =
  {ageList: [D(18), D(25), D(45), D(10), A],
   weightList: [E(98.5), E(81.5), E(70.6), E(98.5), A],
   nameList: [F(&quot;Ada&quot;), F(&quot;Ben&quot;), F(&quot;Caz&quot;), F(&quot;Dan&quot;), F(&quot;Eve&quot;)],
   maleList: [B(false), B(true), A, B(true), B(false)]};
*/

db17.re

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
/* 
type sec =
    G(prim)
  | H(list(sec))
  | I(array(sec))
  | J((string, sec))
  | K({ key: string, value: sec, });
*/

db18.re

exception Unimplemented_type(string);
// exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};
// let secToList: sec =&gt; list(prim) = &lt;fun&gt;;

db19.re

let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};
// let trySecToList: sec =&gt; list(prim) = &lt;fun&gt;;

db2.re

let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
// let toMut: &#x27;a =&gt; mut(&#x27;a) = &lt;fun&gt;;

let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;
// let fromMut: mut(&#x27;a) =&gt; &#x27;a = &lt;fun&gt;;

db20.re

let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}
// let getCounts: list(StringMap.key) =&gt; list((string, int)) = &lt;fun&gt;;

db21.re

let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};
// let getMedian: list(float) =&gt; float = &lt;fun&gt;;

db22.re

let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));
// let getMean: list(float) =&gt; float = &lt;fun&gt;;

db23.re

type stringStats = {
  counts: list((string, int)),
};
// type stringStats = { counts: list((string, int)), };

type floatStats = {
  mean: float,
  median: float,
};
// type floatStats = { mean: float, median: float, };

db24.re

let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};
/*
let listToFloat:
  (list(prim), ~boolAllowed: bool=?, ~intAllowed: bool=?, unit) =&gt; list(float) =
  &lt;fun&gt;;
*/

db25.re

exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};
// let listToString: (list(prim), ~debug: bool=?, unit) =&gt; list(string) = &lt;fun&gt;;

db26.re

let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};
// let getFloatStats: (sec, ~level: int=?, unit) =&gt; floatStats = &lt;fun&gt;;

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}
// let getStringStats: (sec, ~debug: bool=?, unit) =&gt; stringStats = &lt;fun&gt;;

db27.re

let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));
// let primListToSec: list(prim) =&gt; sec = &lt;fun&gt;;

db28.re

let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);
/*
let ages: sec = H([G((D(18))), G((D(25))), G((D(45))), G((D(10))), G(A)]);
let weights: sec =
  H([G((E(98.5))), G((E(81.5))), G((E(70.6))), G((E(98.5))), G(A)]);
let names: sec =
  H([G((F(&quot;Ada&quot;))), G((F(&quot;Ben&quot;))), G((F(&quot;Caz&quot;))), G((F(&quot;Dan&quot;))), G((F(&quot;Eve&quot;)))]);
let males: sec =
  H([G((B(false))), G((B(true))), G(A), G((B(true))), G((B(false)))]);
*/

db29.re

getStringStats(names, ~debug=true, ());
// - : stringStats = {counts: [(&quot;Ada&quot;, 1), (&quot;Ben&quot;, 1), (&quot;Caz&quot;, 1), (&quot;Dan&quot;, 1), (&quot;Eve&quot;, 1)]}

getFloatStats(weights, ~level=1, ());
// - : floatStats = {mean: 87.275, median: 90.}

getStringStats(weights, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;70.6&quot;, 1), (&quot;81.5&quot;, 1), (&quot;98.5&quot;, 2)]}

getFloatStats(ages, ~level=2, ());
// - : floatStats = {mean: 24.5, median: 21.5}

getStringStats(ages, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;10.&quot;, 1), (&quot;18.&quot;, 1), (&quot;25.&quot;, 1), (&quot;45.&quot;, 1)]}

getFloatStats(males, ~level=3, ());
// - : floatStats = {mean: 0.5, median: 0.5}

getStringStats(males, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;0.&quot;, 2), (&quot;1.&quot;, 2)]}

db3.re

let x = ref(0); // Equivalent to let x = toMut(0);
// let x: ref(int) = {contents: 0};

x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);
// - : int = 1

db4.re

type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);
// type prim = A | B(bool) | C(char) | D(int) | E(float) | F(string);

db5.re

let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};
// let change: mut(prim) =&gt; prim = &lt;fun&gt;;

db6.re

let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};
// let toString: mut(prim) =&gt; string = &lt;fun&gt;;

db7.re

let a = toMut(A); toString(a); a.value = change(a); toString(a);
// let a: mut(prim) = {value: A};
// - : string = &quot;empty&quot;
// - : string = &quot;empty&quot;

let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
// let b: mut(prim) = {value: B(false)};
// - : string = &quot;false&quot;
// - : string = &quot;true&quot;

let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
// let c: mut(prim) = {value: C(&#x27;a&#x27;)};
// - : string = &quot;a&quot;
// - : string = &quot;b&quot;

let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
// let d: mut(prim) = {value: D(0)};
// - : string = &quot;0&quot;
// - : string = &quot;+1&quot;

let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
// let e: mut(prim) = {value: E(0.)};
// - : string = &quot;0.&quot;
// - : string = &quot;+1.&quot;

let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);
// let f: mut(prim) = {value: F(&quot;Hello&quot;)};
// - : string = &quot;Hello&quot;
// - : string = &quot;Hello!&quot;

db8.re

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];
/*
let dbRaw: list(array((string, prim))) =
  [[|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(false))|],
   [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)),
     (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)),
     (&quot;alive&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|]];

*/

db9.re

module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});
// module StringMap: { ... };</code></pre><p>Structuring our output, we define types for summarizing string and float data, encapsulating counts for categorical data and central measures for continuous data.</p><pre><code>db.re

/* HANDLING PRIMITIVE TYPES */

// Mutability in ReasonML is a feature primarily used with records. Here&#x27;s how you define a mutable type that can hold any value:
type mut(&#x27;a) = {
  mutable value: &#x27;a,
};

// In λ-calculus, function types like f: A -&gt; B imply a transformation or proof from A to B. The functions toMut and fromMut serve as bridges between mutable and immutable types, showing they can be interchangeable:
let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;

// Using the standard implementation as a reference, you can see how it translates in practical terms:
let x = ref(0); // Equivalent to let x = toMut(0);
x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);

// ReasonML requires explicit type declarations for union types, unlike TypeScript where you might use &quot;int | null&quot;:
type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);

// Variant types in ReasonML, akin to sum types or dependent types in other languages, are exhaustive and unique, ensuring no overlap between types.

// Handling these types necessitates a switch statement, covering all possible variants for completeness:
let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};

// For pattern matching, especially when not all cases are addressed explicitly, the wildcard &quot;_&quot; can be a fallback. The &quot;when&quot; keyword allows for additional conditions in matches, offering a concise way to handle complex patterns:
let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};

// Testing different cases to demonstrate how these functions work with the defined types:
let a = toMut(A); toString(a); a.value = change(a); toString(a);
let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);

/* DATABASE STORAGE FOR DATA SCIENCE */

// Working with generic types and function handling is one thing, but let&#x27;s step into a scenario where the stakes are higher: being data scientists at a medical center, tasked with deriving basic statistics from patient data. Given a raw database in a text file format, we&#x27;ve managed to extract key information as follows:

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];

// The data&#x27;s format is row-wise with an arbitrary order, which could include duplicates, missing, or extra items. To streamline debugging, we&#x27;re aiming to cast these to string maps.

// Here&#x27;s where the Map.Make functor comes into play, allowing us to generate a StringMap keyed by strings for easier readability and manipulation, akin to handling JSON objects:
module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});

// Converting our map to a JSON-like string for debug-friendliness:
let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};

// Transitioning to a generic database format, our row-wise data gets a transformation. Here, we&#x27;re all about clarity and correctness:
let showJson = true;
let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);

// Accessing the elements becomes straightforward. Missing elements? No biggie, we handle that gracefully:
let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};

// After some exploration and analysis, key insights emerge regarding age, weight, name, and gender. These form the cornerstone of our new database signature:
type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};

// Structuring a strictly-typed database while ensuring all necessary keys are included and defaults are set for missing items:
let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);

// Finally, the database is correctly formatted. Next up, transposing this database to a column-wise format, ready for statistical analysis:
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};

// Successfully transposing our data, we&#x27;re set to dive deep into the analysis, equipped with a database that&#x27;s both comprehensive and accurately structured.
let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));

/* STATISTICS LIBRARY DEVELOPMENT */

// Venturing into building a generic statistics library, we&#x27;re focusing on versatility across different data structures. Whether dealing with Lists or Arrays, the goal is seamless integration and handling.

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
  
// The challenge lies in unpacking these varied structures into a consistent format, ideally a list of primitives, for statistical analysis. Given the evolving nature of our library, not all types are fully supported yet, leading to potential exceptions for unhandled cases.
exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};

// To ensure a smooth user experience, we wrap secToList in a function that gracefully handles exceptions, providing clear feedback rather than abrupt errors.
let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};

// Diving into the core of our library, we aim to offer basic but essential statistical functions, each designed to work with a specific type of data.

// getCounts tackles enumeration, mapping each unique string in a list to its frequency of occurrence, ideal for categorical data analysis.
let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}

// getMedian finds the middle value in a list of floats after sorting, a key measure of central tendency for quantitative data.
let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};

// getMean computes the average from a list of floats, providing a quick snapshot of your data&#x27;s central value.
let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));

// Structuring our output, we define types for summarizing string and float data, encapsulating counts for categorical data and central measures for continuous data.
type stringStats = {
  counts: list((string, int)),
};

type floatStats = {
  mean: float,
  median: float,
};

/* DATA ANALYSIS FRAMEWORK */

// Integrating complex data structures into actionable insights requires a systematic approach. We&#x27;ve established methods to deconstruct complex data into primitive lists and have statistical functions ready. The challenge now is to seamlessly connect these components.

// First, let&#x27;s categorize data types based on their analytical utility:

// - Nominal data, like colors &quot;Blue&quot; and &quot;Yellow&quot;, are distinct without a meaningful order. The mode serves as their central tendency measure.
// - Boolean data, a subset of nominal, consists of binary choices like &quot;Yes&quot; and &quot;No&quot;.
// - Ordinal data, such as ratings from 1 (&quot;Low&quot;) to 5 (&quot;High&quot;), imply order but not the uniformity of scale. Their median reflects central tendency.
// - Numeric data, representing continuous or interval data, can be fully quantified. The mean is used to express their central tendency.

// Recognizing that not all operations apply universally across data types underscores the importance of targeted analytical strategies.

// Transitioning to the implementation phase:

// The `listToFloat` function converts a list of primitives to floats, selectively allowing boolean and integer conversions based on flags:
let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};

// Converting primitives to strings while handling incompatible types by casting to floats, then stringifying, allows for flexible data interpretation:
exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};

// `getFloatStats` and `getStringStats` functions then process these lists into statistical summaries, considering the data level restrictions and debug options respectively:
let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}

// Finally, transforming primitive lists to the expected input format for statistical analysis:
let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));

// Extracting statistics becomes straightforward with prepped data:
let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);

// Now, it&#x27;s just a matter of calling the appropriate statistical function for each data type, with optional debugging for string conversions:
getStringStats(names, ~debug=true, ());
getFloatStats(weights, ~level=1, ());
getStringStats(weights, ~debug=true, ());

getFloatStats(ages, ~level=2, ());
getStringStats(ages, ~debug=true, ());

getFloatStats(males, ~level=3, ());
getStringStats(males, ~debug=true, ());

db1.re

type mut(&#x27;a) = {
  mutable value: &#x27;a,
};
// type mut(&#x27;a) = { mutable value: &#x27;a, };

db10.re

let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};
// let mapToJson: StringMap.t(prim) =&gt; string = &lt;fun&gt;;

db11.re

let showJson = true;
// let showJson: bool = true;

let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);
/* let dbGeneric: list(StringMap.t(prim)) =
  [&lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;];
*/
/*
{age: +18, male: false, name: Ada, weight: +98.5}
{age: +25, male: true, name: Ben, weight: +81.5}
{age: +45, alive: true, name: Caz, weight: +70.6}
{age: +10, male: true, name: Dan, weight: +98.5}
{male: false, name: Eve}
*/

db12.re

let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};
// let tryAccessDbGeneric: (StringMap.key, int) =&gt; prim = &lt;fun&gt;;

db13.re

type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};
// type signature = { age: prim, weight: prim, name: prim, male: prim, };

db14.re

let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);
/*
let db: list(signature) =
  [{age: D(18), weight: E(98.5), name: F(&quot;Ada&quot;), male: B(false)},
   {age: D(25), weight: E(81.5), name: F(&quot;Ben&quot;), male: B(true)},
   {age: D(45), weight: E(70.6), name: F(&quot;Caz&quot;), male: A},
   {age: D(10), weight: E(98.5), name: F(&quot;Dan&quot;), male: B(true)},
   {age: A, weight: A, name: F(&quot;Eve&quot;), male: B(false)}];
*/

db15.re

type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
/*
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
*/

db16.re

let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));
/*
let dbCol: signatureColWise =
  {ageList: [D(18), D(25), D(45), D(10), A],
   weightList: [E(98.5), E(81.5), E(70.6), E(98.5), A],
   nameList: [F(&quot;Ada&quot;), F(&quot;Ben&quot;), F(&quot;Caz&quot;), F(&quot;Dan&quot;), F(&quot;Eve&quot;)],
   maleList: [B(false), B(true), A, B(true), B(false)]};
*/

db17.re

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
/* 
type sec =
    G(prim)
  | H(list(sec))
  | I(array(sec))
  | J((string, sec))
  | K({ key: string, value: sec, });
*/

db18.re

exception Unimplemented_type(string);
// exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};
// let secToList: sec =&gt; list(prim) = &lt;fun&gt;;

db19.re

let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};
// let trySecToList: sec =&gt; list(prim) = &lt;fun&gt;;

db2.re

let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
// let toMut: &#x27;a =&gt; mut(&#x27;a) = &lt;fun&gt;;

let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;
// let fromMut: mut(&#x27;a) =&gt; &#x27;a = &lt;fun&gt;;

db20.re

let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}
// let getCounts: list(StringMap.key) =&gt; list((string, int)) = &lt;fun&gt;;

db21.re

let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};
// let getMedian: list(float) =&gt; float = &lt;fun&gt;;

db22.re

let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));
// let getMean: list(float) =&gt; float = &lt;fun&gt;;

db23.re

type stringStats = {
  counts: list((string, int)),
};
// type stringStats = { counts: list((string, int)), };

type floatStats = {
  mean: float,
  median: float,
};
// type floatStats = { mean: float, median: float, };

db24.re

let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};
/*
let listToFloat:
  (list(prim), ~boolAllowed: bool=?, ~intAllowed: bool=?, unit) =&gt; list(float) =
  &lt;fun&gt;;
*/

db25.re

exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};
// let listToString: (list(prim), ~debug: bool=?, unit) =&gt; list(string) = &lt;fun&gt;;

db26.re

let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};
// let getFloatStats: (sec, ~level: int=?, unit) =&gt; floatStats = &lt;fun&gt;;

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}
// let getStringStats: (sec, ~debug: bool=?, unit) =&gt; stringStats = &lt;fun&gt;;

db27.re

let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));
// let primListToSec: list(prim) =&gt; sec = &lt;fun&gt;;

db28.re

let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);
/*
let ages: sec = H([G((D(18))), G((D(25))), G((D(45))), G((D(10))), G(A)]);
let weights: sec =
  H([G((E(98.5))), G((E(81.5))), G((E(70.6))), G((E(98.5))), G(A)]);
let names: sec =
  H([G((F(&quot;Ada&quot;))), G((F(&quot;Ben&quot;))), G((F(&quot;Caz&quot;))), G((F(&quot;Dan&quot;))), G((F(&quot;Eve&quot;)))]);
let males: sec =
  H([G((B(false))), G((B(true))), G(A), G((B(true))), G((B(false)))]);
*/

db29.re

getStringStats(names, ~debug=true, ());
// - : stringStats = {counts: [(&quot;Ada&quot;, 1), (&quot;Ben&quot;, 1), (&quot;Caz&quot;, 1), (&quot;Dan&quot;, 1), (&quot;Eve&quot;, 1)]}

getFloatStats(weights, ~level=1, ());
// - : floatStats = {mean: 87.275, median: 90.}

getStringStats(weights, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;70.6&quot;, 1), (&quot;81.5&quot;, 1), (&quot;98.5&quot;, 2)]}

getFloatStats(ages, ~level=2, ());
// - : floatStats = {mean: 24.5, median: 21.5}

getStringStats(ages, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;10.&quot;, 1), (&quot;18.&quot;, 1), (&quot;25.&quot;, 1), (&quot;45.&quot;, 1)]}

getFloatStats(males, ~level=3, ());
// - : floatStats = {mean: 0.5, median: 0.5}

getStringStats(males, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;0.&quot;, 2), (&quot;1.&quot;, 2)]}

db3.re

let x = ref(0); // Equivalent to let x = toMut(0);
// let x: ref(int) = {contents: 0};

x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);
// - : int = 1

db4.re

type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);
// type prim = A | B(bool) | C(char) | D(int) | E(float) | F(string);

db5.re

let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};
// let change: mut(prim) =&gt; prim = &lt;fun&gt;;

db6.re

let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};
// let toString: mut(prim) =&gt; string = &lt;fun&gt;;

db7.re

let a = toMut(A); toString(a); a.value = change(a); toString(a);
// let a: mut(prim) = {value: A};
// - : string = &quot;empty&quot;
// - : string = &quot;empty&quot;

let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
// let b: mut(prim) = {value: B(false)};
// - : string = &quot;false&quot;
// - : string = &quot;true&quot;

let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
// let c: mut(prim) = {value: C(&#x27;a&#x27;)};
// - : string = &quot;a&quot;
// - : string = &quot;b&quot;

let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
// let d: mut(prim) = {value: D(0)};
// - : string = &quot;0&quot;
// - : string = &quot;+1&quot;

let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
// let e: mut(prim) = {value: E(0.)};
// - : string = &quot;0.&quot;
// - : string = &quot;+1.&quot;

let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);
// let f: mut(prim) = {value: F(&quot;Hello&quot;)};
// - : string = &quot;Hello&quot;
// - : string = &quot;Hello!&quot;

db8.re

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];
/*
let dbRaw: list(array((string, prim))) =
  [[|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(false))|],
   [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)),
     (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)),
     (&quot;alive&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|]];

*/

db9.re

module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});
// module StringMap: { ... };</code></pre><h4>Data Analysis</h4><figure><img alt="" src="https://cdn-images-1.medium.com/max/1400/1*2rhPAXbsOfuVt13i_Ue-QA.png" /><figcaption>Source: What is Exploratory Data Analysis?, towardsdatascience.com</figcaption></figure><p>Integrating complex data structures into actionable insights requires a systematic approach. We’ve established methods to deconstruct complex data into primitive lists and have statistical functions ready. The challenge now is to seamlessly connect these components.</p><p>First, let’s categorize data types based on their analytical utility:</p><ul><li>Nominal data, like colors “Blue” and “Yellow”, are distinct without a meaningful order. The mode serves as their central tendency measure.</li><li>Boolean data, a subset of nominal, consists of binary choices like “Yes” and “No”.</li><li>Ordinal data, such as ratings from 1 (“Low”) to 5 (“High”), imply order but not the uniformity of scale. Their median reflects central tendency.</li><li>Numeric data, representing continuous or interval data, can be fully quantified. The mean is used to express their central tendency.</li></ul><figure><img alt="" src="https://cdn-images-1.medium.com/max/1400/1*dSrvbjS5SdPQzKuutuF3AA.png" /><figcaption>Source: Nominal, Ordinal, Interval and Ratio Data, Microbe Notes</figcaption></figure><p>Recognizing that not all operations apply universally across data types underscores the importance of targeted analytical strategies.</p><p>Transitioning to the implementation phase:</p><p>The `listToFloat` function converts a list of primitives to floats, selectively allowing boolean and integer conversions based on flags:</p><pre><code>db.re

/* HANDLING PRIMITIVE TYPES */

// Mutability in ReasonML is a feature primarily used with records. Here&#x27;s how you define a mutable type that can hold any value:
type mut(&#x27;a) = {
  mutable value: &#x27;a,
};

// In λ-calculus, function types like f: A -&gt; B imply a transformation or proof from A to B. The functions toMut and fromMut serve as bridges between mutable and immutable types, showing they can be interchangeable:
let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;

// Using the standard implementation as a reference, you can see how it translates in practical terms:
let x = ref(0); // Equivalent to let x = toMut(0);
x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);

// ReasonML requires explicit type declarations for union types, unlike TypeScript where you might use &quot;int | null&quot;:
type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);

// Variant types in ReasonML, akin to sum types or dependent types in other languages, are exhaustive and unique, ensuring no overlap between types.

// Handling these types necessitates a switch statement, covering all possible variants for completeness:
let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};

// For pattern matching, especially when not all cases are addressed explicitly, the wildcard &quot;_&quot; can be a fallback. The &quot;when&quot; keyword allows for additional conditions in matches, offering a concise way to handle complex patterns:
let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};

// Testing different cases to demonstrate how these functions work with the defined types:
let a = toMut(A); toString(a); a.value = change(a); toString(a);
let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);

/* DATABASE STORAGE FOR DATA SCIENCE */

// Working with generic types and function handling is one thing, but let&#x27;s step into a scenario where the stakes are higher: being data scientists at a medical center, tasked with deriving basic statistics from patient data. Given a raw database in a text file format, we&#x27;ve managed to extract key information as follows:

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];

// The data&#x27;s format is row-wise with an arbitrary order, which could include duplicates, missing, or extra items. To streamline debugging, we&#x27;re aiming to cast these to string maps.

// Here&#x27;s where the Map.Make functor comes into play, allowing us to generate a StringMap keyed by strings for easier readability and manipulation, akin to handling JSON objects:
module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});

// Converting our map to a JSON-like string for debug-friendliness:
let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};

// Transitioning to a generic database format, our row-wise data gets a transformation. Here, we&#x27;re all about clarity and correctness:
let showJson = true;
let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);

// Accessing the elements becomes straightforward. Missing elements? No biggie, we handle that gracefully:
let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};

// After some exploration and analysis, key insights emerge regarding age, weight, name, and gender. These form the cornerstone of our new database signature:
type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};

// Structuring a strictly-typed database while ensuring all necessary keys are included and defaults are set for missing items:
let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);

// Finally, the database is correctly formatted. Next up, transposing this database to a column-wise format, ready for statistical analysis:
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};

// Successfully transposing our data, we&#x27;re set to dive deep into the analysis, equipped with a database that&#x27;s both comprehensive and accurately structured.
let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));

/* STATISTICS LIBRARY DEVELOPMENT */

// Venturing into building a generic statistics library, we&#x27;re focusing on versatility across different data structures. Whether dealing with Lists or Arrays, the goal is seamless integration and handling.

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
  
// The challenge lies in unpacking these varied structures into a consistent format, ideally a list of primitives, for statistical analysis. Given the evolving nature of our library, not all types are fully supported yet, leading to potential exceptions for unhandled cases.
exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};

// To ensure a smooth user experience, we wrap secToList in a function that gracefully handles exceptions, providing clear feedback rather than abrupt errors.
let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};

// Diving into the core of our library, we aim to offer basic but essential statistical functions, each designed to work with a specific type of data.

// getCounts tackles enumeration, mapping each unique string in a list to its frequency of occurrence, ideal for categorical data analysis.
let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}

// getMedian finds the middle value in a list of floats after sorting, a key measure of central tendency for quantitative data.
let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};

// getMean computes the average from a list of floats, providing a quick snapshot of your data&#x27;s central value.
let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));

// Structuring our output, we define types for summarizing string and float data, encapsulating counts for categorical data and central measures for continuous data.
type stringStats = {
  counts: list((string, int)),
};

type floatStats = {
  mean: float,
  median: float,
};

/* DATA ANALYSIS FRAMEWORK */

// Integrating complex data structures into actionable insights requires a systematic approach. We&#x27;ve established methods to deconstruct complex data into primitive lists and have statistical functions ready. The challenge now is to seamlessly connect these components.

// First, let&#x27;s categorize data types based on their analytical utility:

// - Nominal data, like colors &quot;Blue&quot; and &quot;Yellow&quot;, are distinct without a meaningful order. The mode serves as their central tendency measure.
// - Boolean data, a subset of nominal, consists of binary choices like &quot;Yes&quot; and &quot;No&quot;.
// - Ordinal data, such as ratings from 1 (&quot;Low&quot;) to 5 (&quot;High&quot;), imply order but not the uniformity of scale. Their median reflects central tendency.
// - Numeric data, representing continuous or interval data, can be fully quantified. The mean is used to express their central tendency.

// Recognizing that not all operations apply universally across data types underscores the importance of targeted analytical strategies.

// Transitioning to the implementation phase:

// The `listToFloat` function converts a list of primitives to floats, selectively allowing boolean and integer conversions based on flags:
let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};

// Converting primitives to strings while handling incompatible types by casting to floats, then stringifying, allows for flexible data interpretation:
exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};

// `getFloatStats` and `getStringStats` functions then process these lists into statistical summaries, considering the data level restrictions and debug options respectively:
let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}

// Finally, transforming primitive lists to the expected input format for statistical analysis:
let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));

// Extracting statistics becomes straightforward with prepped data:
let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);

// Now, it&#x27;s just a matter of calling the appropriate statistical function for each data type, with optional debugging for string conversions:
getStringStats(names, ~debug=true, ());
getFloatStats(weights, ~level=1, ());
getStringStats(weights, ~debug=true, ());

getFloatStats(ages, ~level=2, ());
getStringStats(ages, ~debug=true, ());

getFloatStats(males, ~level=3, ());
getStringStats(males, ~debug=true, ());

db1.re

type mut(&#x27;a) = {
  mutable value: &#x27;a,
};
// type mut(&#x27;a) = { mutable value: &#x27;a, };

db10.re

let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};
// let mapToJson: StringMap.t(prim) =&gt; string = &lt;fun&gt;;

db11.re

let showJson = true;
// let showJson: bool = true;

let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);
/* let dbGeneric: list(StringMap.t(prim)) =
  [&lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;];
*/
/*
{age: +18, male: false, name: Ada, weight: +98.5}
{age: +25, male: true, name: Ben, weight: +81.5}
{age: +45, alive: true, name: Caz, weight: +70.6}
{age: +10, male: true, name: Dan, weight: +98.5}
{male: false, name: Eve}
*/

db12.re

let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};
// let tryAccessDbGeneric: (StringMap.key, int) =&gt; prim = &lt;fun&gt;;

db13.re

type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};
// type signature = { age: prim, weight: prim, name: prim, male: prim, };

db14.re

let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);
/*
let db: list(signature) =
  [{age: D(18), weight: E(98.5), name: F(&quot;Ada&quot;), male: B(false)},
   {age: D(25), weight: E(81.5), name: F(&quot;Ben&quot;), male: B(true)},
   {age: D(45), weight: E(70.6), name: F(&quot;Caz&quot;), male: A},
   {age: D(10), weight: E(98.5), name: F(&quot;Dan&quot;), male: B(true)},
   {age: A, weight: A, name: F(&quot;Eve&quot;), male: B(false)}];
*/

db15.re

type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
/*
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
*/

db16.re

let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));
/*
let dbCol: signatureColWise =
  {ageList: [D(18), D(25), D(45), D(10), A],
   weightList: [E(98.5), E(81.5), E(70.6), E(98.5), A],
   nameList: [F(&quot;Ada&quot;), F(&quot;Ben&quot;), F(&quot;Caz&quot;), F(&quot;Dan&quot;), F(&quot;Eve&quot;)],
   maleList: [B(false), B(true), A, B(true), B(false)]};
*/

db17.re

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
/* 
type sec =
    G(prim)
  | H(list(sec))
  | I(array(sec))
  | J((string, sec))
  | K({ key: string, value: sec, });
*/

db18.re

exception Unimplemented_type(string);
// exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};
// let secToList: sec =&gt; list(prim) = &lt;fun&gt;;

db19.re

let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};
// let trySecToList: sec =&gt; list(prim) = &lt;fun&gt;;

db2.re

let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
// let toMut: &#x27;a =&gt; mut(&#x27;a) = &lt;fun&gt;;

let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;
// let fromMut: mut(&#x27;a) =&gt; &#x27;a = &lt;fun&gt;;

db20.re

let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}
// let getCounts: list(StringMap.key) =&gt; list((string, int)) = &lt;fun&gt;;

db21.re

let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};
// let getMedian: list(float) =&gt; float = &lt;fun&gt;;

db22.re

let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));
// let getMean: list(float) =&gt; float = &lt;fun&gt;;

db23.re

type stringStats = {
  counts: list((string, int)),
};
// type stringStats = { counts: list((string, int)), };

type floatStats = {
  mean: float,
  median: float,
};
// type floatStats = { mean: float, median: float, };

db24.re

let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};
/*
let listToFloat:
  (list(prim), ~boolAllowed: bool=?, ~intAllowed: bool=?, unit) =&gt; list(float) =
  &lt;fun&gt;;
*/

db25.re

exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};
// let listToString: (list(prim), ~debug: bool=?, unit) =&gt; list(string) = &lt;fun&gt;;

db26.re

let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};
// let getFloatStats: (sec, ~level: int=?, unit) =&gt; floatStats = &lt;fun&gt;;

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}
// let getStringStats: (sec, ~debug: bool=?, unit) =&gt; stringStats = &lt;fun&gt;;

db27.re

let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));
// let primListToSec: list(prim) =&gt; sec = &lt;fun&gt;;

db28.re

let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);
/*
let ages: sec = H([G((D(18))), G((D(25))), G((D(45))), G((D(10))), G(A)]);
let weights: sec =
  H([G((E(98.5))), G((E(81.5))), G((E(70.6))), G((E(98.5))), G(A)]);
let names: sec =
  H([G((F(&quot;Ada&quot;))), G((F(&quot;Ben&quot;))), G((F(&quot;Caz&quot;))), G((F(&quot;Dan&quot;))), G((F(&quot;Eve&quot;)))]);
let males: sec =
  H([G((B(false))), G((B(true))), G(A), G((B(true))), G((B(false)))]);
*/

db29.re

getStringStats(names, ~debug=true, ());
// - : stringStats = {counts: [(&quot;Ada&quot;, 1), (&quot;Ben&quot;, 1), (&quot;Caz&quot;, 1), (&quot;Dan&quot;, 1), (&quot;Eve&quot;, 1)]}

getFloatStats(weights, ~level=1, ());
// - : floatStats = {mean: 87.275, median: 90.}

getStringStats(weights, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;70.6&quot;, 1), (&quot;81.5&quot;, 1), (&quot;98.5&quot;, 2)]}

getFloatStats(ages, ~level=2, ());
// - : floatStats = {mean: 24.5, median: 21.5}

getStringStats(ages, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;10.&quot;, 1), (&quot;18.&quot;, 1), (&quot;25.&quot;, 1), (&quot;45.&quot;, 1)]}

getFloatStats(males, ~level=3, ());
// - : floatStats = {mean: 0.5, median: 0.5}

getStringStats(males, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;0.&quot;, 2), (&quot;1.&quot;, 2)]}

db3.re

let x = ref(0); // Equivalent to let x = toMut(0);
// let x: ref(int) = {contents: 0};

x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);
// - : int = 1

db4.re

type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);
// type prim = A | B(bool) | C(char) | D(int) | E(float) | F(string);

db5.re

let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};
// let change: mut(prim) =&gt; prim = &lt;fun&gt;;

db6.re

let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};
// let toString: mut(prim) =&gt; string = &lt;fun&gt;;

db7.re

let a = toMut(A); toString(a); a.value = change(a); toString(a);
// let a: mut(prim) = {value: A};
// - : string = &quot;empty&quot;
// - : string = &quot;empty&quot;

let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
// let b: mut(prim) = {value: B(false)};
// - : string = &quot;false&quot;
// - : string = &quot;true&quot;

let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
// let c: mut(prim) = {value: C(&#x27;a&#x27;)};
// - : string = &quot;a&quot;
// - : string = &quot;b&quot;

let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
// let d: mut(prim) = {value: D(0)};
// - : string = &quot;0&quot;
// - : string = &quot;+1&quot;

let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
// let e: mut(prim) = {value: E(0.)};
// - : string = &quot;0.&quot;
// - : string = &quot;+1.&quot;

let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);
// let f: mut(prim) = {value: F(&quot;Hello&quot;)};
// - : string = &quot;Hello&quot;
// - : string = &quot;Hello!&quot;

db8.re

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];
/*
let dbRaw: list(array((string, prim))) =
  [[|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(false))|],
   [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)),
     (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)),
     (&quot;alive&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|]];

*/

db9.re

module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});
// module StringMap: { ... };</code></pre><p>Converting primitives to strings while handling incompatible types by casting to floats, then stringifying, allows for flexible data interpretation:</p><pre><code>db.re

/* HANDLING PRIMITIVE TYPES */

// Mutability in ReasonML is a feature primarily used with records. Here&#x27;s how you define a mutable type that can hold any value:
type mut(&#x27;a) = {
  mutable value: &#x27;a,
};

// In λ-calculus, function types like f: A -&gt; B imply a transformation or proof from A to B. The functions toMut and fromMut serve as bridges between mutable and immutable types, showing they can be interchangeable:
let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;

// Using the standard implementation as a reference, you can see how it translates in practical terms:
let x = ref(0); // Equivalent to let x = toMut(0);
x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);

// ReasonML requires explicit type declarations for union types, unlike TypeScript where you might use &quot;int | null&quot;:
type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);

// Variant types in ReasonML, akin to sum types or dependent types in other languages, are exhaustive and unique, ensuring no overlap between types.

// Handling these types necessitates a switch statement, covering all possible variants for completeness:
let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};

// For pattern matching, especially when not all cases are addressed explicitly, the wildcard &quot;_&quot; can be a fallback. The &quot;when&quot; keyword allows for additional conditions in matches, offering a concise way to handle complex patterns:
let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};

// Testing different cases to demonstrate how these functions work with the defined types:
let a = toMut(A); toString(a); a.value = change(a); toString(a);
let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);

/* DATABASE STORAGE FOR DATA SCIENCE */

// Working with generic types and function handling is one thing, but let&#x27;s step into a scenario where the stakes are higher: being data scientists at a medical center, tasked with deriving basic statistics from patient data. Given a raw database in a text file format, we&#x27;ve managed to extract key information as follows:

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];

// The data&#x27;s format is row-wise with an arbitrary order, which could include duplicates, missing, or extra items. To streamline debugging, we&#x27;re aiming to cast these to string maps.

// Here&#x27;s where the Map.Make functor comes into play, allowing us to generate a StringMap keyed by strings for easier readability and manipulation, akin to handling JSON objects:
module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});

// Converting our map to a JSON-like string for debug-friendliness:
let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};

// Transitioning to a generic database format, our row-wise data gets a transformation. Here, we&#x27;re all about clarity and correctness:
let showJson = true;
let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);

// Accessing the elements becomes straightforward. Missing elements? No biggie, we handle that gracefully:
let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};

// After some exploration and analysis, key insights emerge regarding age, weight, name, and gender. These form the cornerstone of our new database signature:
type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};

// Structuring a strictly-typed database while ensuring all necessary keys are included and defaults are set for missing items:
let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);

// Finally, the database is correctly formatted. Next up, transposing this database to a column-wise format, ready for statistical analysis:
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};

// Successfully transposing our data, we&#x27;re set to dive deep into the analysis, equipped with a database that&#x27;s both comprehensive and accurately structured.
let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));

/* STATISTICS LIBRARY DEVELOPMENT */

// Venturing into building a generic statistics library, we&#x27;re focusing on versatility across different data structures. Whether dealing with Lists or Arrays, the goal is seamless integration and handling.

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
  
// The challenge lies in unpacking these varied structures into a consistent format, ideally a list of primitives, for statistical analysis. Given the evolving nature of our library, not all types are fully supported yet, leading to potential exceptions for unhandled cases.
exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};

// To ensure a smooth user experience, we wrap secToList in a function that gracefully handles exceptions, providing clear feedback rather than abrupt errors.
let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};

// Diving into the core of our library, we aim to offer basic but essential statistical functions, each designed to work with a specific type of data.

// getCounts tackles enumeration, mapping each unique string in a list to its frequency of occurrence, ideal for categorical data analysis.
let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}

// getMedian finds the middle value in a list of floats after sorting, a key measure of central tendency for quantitative data.
let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};

// getMean computes the average from a list of floats, providing a quick snapshot of your data&#x27;s central value.
let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));

// Structuring our output, we define types for summarizing string and float data, encapsulating counts for categorical data and central measures for continuous data.
type stringStats = {
  counts: list((string, int)),
};

type floatStats = {
  mean: float,
  median: float,
};

/* DATA ANALYSIS FRAMEWORK */

// Integrating complex data structures into actionable insights requires a systematic approach. We&#x27;ve established methods to deconstruct complex data into primitive lists and have statistical functions ready. The challenge now is to seamlessly connect these components.

// First, let&#x27;s categorize data types based on their analytical utility:

// - Nominal data, like colors &quot;Blue&quot; and &quot;Yellow&quot;, are distinct without a meaningful order. The mode serves as their central tendency measure.
// - Boolean data, a subset of nominal, consists of binary choices like &quot;Yes&quot; and &quot;No&quot;.
// - Ordinal data, such as ratings from 1 (&quot;Low&quot;) to 5 (&quot;High&quot;), imply order but not the uniformity of scale. Their median reflects central tendency.
// - Numeric data, representing continuous or interval data, can be fully quantified. The mean is used to express their central tendency.

// Recognizing that not all operations apply universally across data types underscores the importance of targeted analytical strategies.

// Transitioning to the implementation phase:

// The `listToFloat` function converts a list of primitives to floats, selectively allowing boolean and integer conversions based on flags:
let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};

// Converting primitives to strings while handling incompatible types by casting to floats, then stringifying, allows for flexible data interpretation:
exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};

// `getFloatStats` and `getStringStats` functions then process these lists into statistical summaries, considering the data level restrictions and debug options respectively:
let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}

// Finally, transforming primitive lists to the expected input format for statistical analysis:
let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));

// Extracting statistics becomes straightforward with prepped data:
let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);

// Now, it&#x27;s just a matter of calling the appropriate statistical function for each data type, with optional debugging for string conversions:
getStringStats(names, ~debug=true, ());
getFloatStats(weights, ~level=1, ());
getStringStats(weights, ~debug=true, ());

getFloatStats(ages, ~level=2, ());
getStringStats(ages, ~debug=true, ());

getFloatStats(males, ~level=3, ());
getStringStats(males, ~debug=true, ());

db1.re

type mut(&#x27;a) = {
  mutable value: &#x27;a,
};
// type mut(&#x27;a) = { mutable value: &#x27;a, };

db10.re

let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};
// let mapToJson: StringMap.t(prim) =&gt; string = &lt;fun&gt;;

db11.re

let showJson = true;
// let showJson: bool = true;

let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);
/* let dbGeneric: list(StringMap.t(prim)) =
  [&lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;];
*/
/*
{age: +18, male: false, name: Ada, weight: +98.5}
{age: +25, male: true, name: Ben, weight: +81.5}
{age: +45, alive: true, name: Caz, weight: +70.6}
{age: +10, male: true, name: Dan, weight: +98.5}
{male: false, name: Eve}
*/

db12.re

let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};
// let tryAccessDbGeneric: (StringMap.key, int) =&gt; prim = &lt;fun&gt;;

db13.re

type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};
// type signature = { age: prim, weight: prim, name: prim, male: prim, };

db14.re

let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);
/*
let db: list(signature) =
  [{age: D(18), weight: E(98.5), name: F(&quot;Ada&quot;), male: B(false)},
   {age: D(25), weight: E(81.5), name: F(&quot;Ben&quot;), male: B(true)},
   {age: D(45), weight: E(70.6), name: F(&quot;Caz&quot;), male: A},
   {age: D(10), weight: E(98.5), name: F(&quot;Dan&quot;), male: B(true)},
   {age: A, weight: A, name: F(&quot;Eve&quot;), male: B(false)}];
*/

db15.re

type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
/*
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
*/

db16.re

let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));
/*
let dbCol: signatureColWise =
  {ageList: [D(18), D(25), D(45), D(10), A],
   weightList: [E(98.5), E(81.5), E(70.6), E(98.5), A],
   nameList: [F(&quot;Ada&quot;), F(&quot;Ben&quot;), F(&quot;Caz&quot;), F(&quot;Dan&quot;), F(&quot;Eve&quot;)],
   maleList: [B(false), B(true), A, B(true), B(false)]};
*/

db17.re

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
/* 
type sec =
    G(prim)
  | H(list(sec))
  | I(array(sec))
  | J((string, sec))
  | K({ key: string, value: sec, });
*/

db18.re

exception Unimplemented_type(string);
// exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};
// let secToList: sec =&gt; list(prim) = &lt;fun&gt;;

db19.re

let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};
// let trySecToList: sec =&gt; list(prim) = &lt;fun&gt;;

db2.re

let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
// let toMut: &#x27;a =&gt; mut(&#x27;a) = &lt;fun&gt;;

let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;
// let fromMut: mut(&#x27;a) =&gt; &#x27;a = &lt;fun&gt;;

db20.re

let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}
// let getCounts: list(StringMap.key) =&gt; list((string, int)) = &lt;fun&gt;;

db21.re

let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};
// let getMedian: list(float) =&gt; float = &lt;fun&gt;;

db22.re

let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));
// let getMean: list(float) =&gt; float = &lt;fun&gt;;

db23.re

type stringStats = {
  counts: list((string, int)),
};
// type stringStats = { counts: list((string, int)), };

type floatStats = {
  mean: float,
  median: float,
};
// type floatStats = { mean: float, median: float, };

db24.re

let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};
/*
let listToFloat:
  (list(prim), ~boolAllowed: bool=?, ~intAllowed: bool=?, unit) =&gt; list(float) =
  &lt;fun&gt;;
*/

db25.re

exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};
// let listToString: (list(prim), ~debug: bool=?, unit) =&gt; list(string) = &lt;fun&gt;;

db26.re

let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};
// let getFloatStats: (sec, ~level: int=?, unit) =&gt; floatStats = &lt;fun&gt;;

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}
// let getStringStats: (sec, ~debug: bool=?, unit) =&gt; stringStats = &lt;fun&gt;;

db27.re

let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));
// let primListToSec: list(prim) =&gt; sec = &lt;fun&gt;;

db28.re

let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);
/*
let ages: sec = H([G((D(18))), G((D(25))), G((D(45))), G((D(10))), G(A)]);
let weights: sec =
  H([G((E(98.5))), G((E(81.5))), G((E(70.6))), G((E(98.5))), G(A)]);
let names: sec =
  H([G((F(&quot;Ada&quot;))), G((F(&quot;Ben&quot;))), G((F(&quot;Caz&quot;))), G((F(&quot;Dan&quot;))), G((F(&quot;Eve&quot;)))]);
let males: sec =
  H([G((B(false))), G((B(true))), G(A), G((B(true))), G((B(false)))]);
*/

db29.re

getStringStats(names, ~debug=true, ());
// - : stringStats = {counts: [(&quot;Ada&quot;, 1), (&quot;Ben&quot;, 1), (&quot;Caz&quot;, 1), (&quot;Dan&quot;, 1), (&quot;Eve&quot;, 1)]}

getFloatStats(weights, ~level=1, ());
// - : floatStats = {mean: 87.275, median: 90.}

getStringStats(weights, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;70.6&quot;, 1), (&quot;81.5&quot;, 1), (&quot;98.5&quot;, 2)]}

getFloatStats(ages, ~level=2, ());
// - : floatStats = {mean: 24.5, median: 21.5}

getStringStats(ages, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;10.&quot;, 1), (&quot;18.&quot;, 1), (&quot;25.&quot;, 1), (&quot;45.&quot;, 1)]}

getFloatStats(males, ~level=3, ());
// - : floatStats = {mean: 0.5, median: 0.5}

getStringStats(males, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;0.&quot;, 2), (&quot;1.&quot;, 2)]}

db3.re

let x = ref(0); // Equivalent to let x = toMut(0);
// let x: ref(int) = {contents: 0};

x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);
// - : int = 1

db4.re

type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);
// type prim = A | B(bool) | C(char) | D(int) | E(float) | F(string);

db5.re

let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};
// let change: mut(prim) =&gt; prim = &lt;fun&gt;;

db6.re

let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};
// let toString: mut(prim) =&gt; string = &lt;fun&gt;;

db7.re

let a = toMut(A); toString(a); a.value = change(a); toString(a);
// let a: mut(prim) = {value: A};
// - : string = &quot;empty&quot;
// - : string = &quot;empty&quot;

let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
// let b: mut(prim) = {value: B(false)};
// - : string = &quot;false&quot;
// - : string = &quot;true&quot;

let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
// let c: mut(prim) = {value: C(&#x27;a&#x27;)};
// - : string = &quot;a&quot;
// - : string = &quot;b&quot;

let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
// let d: mut(prim) = {value: D(0)};
// - : string = &quot;0&quot;
// - : string = &quot;+1&quot;

let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
// let e: mut(prim) = {value: E(0.)};
// - : string = &quot;0.&quot;
// - : string = &quot;+1.&quot;

let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);
// let f: mut(prim) = {value: F(&quot;Hello&quot;)};
// - : string = &quot;Hello&quot;
// - : string = &quot;Hello!&quot;

db8.re

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];
/*
let dbRaw: list(array((string, prim))) =
  [[|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(false))|],
   [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)),
     (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)),
     (&quot;alive&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|]];

*/

db9.re

module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});
// module StringMap: { ... };</code></pre><p>`getFloatStats` and `getStringStats` functions then process these lists into statistical summaries, considering the data level restrictions and debug options respectively:</p><pre><code>db.re

/* HANDLING PRIMITIVE TYPES */

// Mutability in ReasonML is a feature primarily used with records. Here&#x27;s how you define a mutable type that can hold any value:
type mut(&#x27;a) = {
  mutable value: &#x27;a,
};

// In λ-calculus, function types like f: A -&gt; B imply a transformation or proof from A to B. The functions toMut and fromMut serve as bridges between mutable and immutable types, showing they can be interchangeable:
let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;

// Using the standard implementation as a reference, you can see how it translates in practical terms:
let x = ref(0); // Equivalent to let x = toMut(0);
x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);

// ReasonML requires explicit type declarations for union types, unlike TypeScript where you might use &quot;int | null&quot;:
type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);

// Variant types in ReasonML, akin to sum types or dependent types in other languages, are exhaustive and unique, ensuring no overlap between types.

// Handling these types necessitates a switch statement, covering all possible variants for completeness:
let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};

// For pattern matching, especially when not all cases are addressed explicitly, the wildcard &quot;_&quot; can be a fallback. The &quot;when&quot; keyword allows for additional conditions in matches, offering a concise way to handle complex patterns:
let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};

// Testing different cases to demonstrate how these functions work with the defined types:
let a = toMut(A); toString(a); a.value = change(a); toString(a);
let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);

/* DATABASE STORAGE FOR DATA SCIENCE */

// Working with generic types and function handling is one thing, but let&#x27;s step into a scenario where the stakes are higher: being data scientists at a medical center, tasked with deriving basic statistics from patient data. Given a raw database in a text file format, we&#x27;ve managed to extract key information as follows:

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];

// The data&#x27;s format is row-wise with an arbitrary order, which could include duplicates, missing, or extra items. To streamline debugging, we&#x27;re aiming to cast these to string maps.

// Here&#x27;s where the Map.Make functor comes into play, allowing us to generate a StringMap keyed by strings for easier readability and manipulation, akin to handling JSON objects:
module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});

// Converting our map to a JSON-like string for debug-friendliness:
let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};

// Transitioning to a generic database format, our row-wise data gets a transformation. Here, we&#x27;re all about clarity and correctness:
let showJson = true;
let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);

// Accessing the elements becomes straightforward. Missing elements? No biggie, we handle that gracefully:
let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};

// After some exploration and analysis, key insights emerge regarding age, weight, name, and gender. These form the cornerstone of our new database signature:
type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};

// Structuring a strictly-typed database while ensuring all necessary keys are included and defaults are set for missing items:
let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);

// Finally, the database is correctly formatted. Next up, transposing this database to a column-wise format, ready for statistical analysis:
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};

// Successfully transposing our data, we&#x27;re set to dive deep into the analysis, equipped with a database that&#x27;s both comprehensive and accurately structured.
let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));

/* STATISTICS LIBRARY DEVELOPMENT */

// Venturing into building a generic statistics library, we&#x27;re focusing on versatility across different data structures. Whether dealing with Lists or Arrays, the goal is seamless integration and handling.

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
  
// The challenge lies in unpacking these varied structures into a consistent format, ideally a list of primitives, for statistical analysis. Given the evolving nature of our library, not all types are fully supported yet, leading to potential exceptions for unhandled cases.
exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};

// To ensure a smooth user experience, we wrap secToList in a function that gracefully handles exceptions, providing clear feedback rather than abrupt errors.
let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};

// Diving into the core of our library, we aim to offer basic but essential statistical functions, each designed to work with a specific type of data.

// getCounts tackles enumeration, mapping each unique string in a list to its frequency of occurrence, ideal for categorical data analysis.
let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}

// getMedian finds the middle value in a list of floats after sorting, a key measure of central tendency for quantitative data.
let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};

// getMean computes the average from a list of floats, providing a quick snapshot of your data&#x27;s central value.
let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));

// Structuring our output, we define types for summarizing string and float data, encapsulating counts for categorical data and central measures for continuous data.
type stringStats = {
  counts: list((string, int)),
};

type floatStats = {
  mean: float,
  median: float,
};

/* DATA ANALYSIS FRAMEWORK */

// Integrating complex data structures into actionable insights requires a systematic approach. We&#x27;ve established methods to deconstruct complex data into primitive lists and have statistical functions ready. The challenge now is to seamlessly connect these components.

// First, let&#x27;s categorize data types based on their analytical utility:

// - Nominal data, like colors &quot;Blue&quot; and &quot;Yellow&quot;, are distinct without a meaningful order. The mode serves as their central tendency measure.
// - Boolean data, a subset of nominal, consists of binary choices like &quot;Yes&quot; and &quot;No&quot;.
// - Ordinal data, such as ratings from 1 (&quot;Low&quot;) to 5 (&quot;High&quot;), imply order but not the uniformity of scale. Their median reflects central tendency.
// - Numeric data, representing continuous or interval data, can be fully quantified. The mean is used to express their central tendency.

// Recognizing that not all operations apply universally across data types underscores the importance of targeted analytical strategies.

// Transitioning to the implementation phase:

// The `listToFloat` function converts a list of primitives to floats, selectively allowing boolean and integer conversions based on flags:
let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};

// Converting primitives to strings while handling incompatible types by casting to floats, then stringifying, allows for flexible data interpretation:
exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};

// `getFloatStats` and `getStringStats` functions then process these lists into statistical summaries, considering the data level restrictions and debug options respectively:
let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}

// Finally, transforming primitive lists to the expected input format for statistical analysis:
let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));

// Extracting statistics becomes straightforward with prepped data:
let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);

// Now, it&#x27;s just a matter of calling the appropriate statistical function for each data type, with optional debugging for string conversions:
getStringStats(names, ~debug=true, ());
getFloatStats(weights, ~level=1, ());
getStringStats(weights, ~debug=true, ());

getFloatStats(ages, ~level=2, ());
getStringStats(ages, ~debug=true, ());

getFloatStats(males, ~level=3, ());
getStringStats(males, ~debug=true, ());

db1.re

type mut(&#x27;a) = {
  mutable value: &#x27;a,
};
// type mut(&#x27;a) = { mutable value: &#x27;a, };

db10.re

let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};
// let mapToJson: StringMap.t(prim) =&gt; string = &lt;fun&gt;;

db11.re

let showJson = true;
// let showJson: bool = true;

let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);
/* let dbGeneric: list(StringMap.t(prim)) =
  [&lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;];
*/
/*
{age: +18, male: false, name: Ada, weight: +98.5}
{age: +25, male: true, name: Ben, weight: +81.5}
{age: +45, alive: true, name: Caz, weight: +70.6}
{age: +10, male: true, name: Dan, weight: +98.5}
{male: false, name: Eve}
*/

db12.re

let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};
// let tryAccessDbGeneric: (StringMap.key, int) =&gt; prim = &lt;fun&gt;;

db13.re

type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};
// type signature = { age: prim, weight: prim, name: prim, male: prim, };

db14.re

let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);
/*
let db: list(signature) =
  [{age: D(18), weight: E(98.5), name: F(&quot;Ada&quot;), male: B(false)},
   {age: D(25), weight: E(81.5), name: F(&quot;Ben&quot;), male: B(true)},
   {age: D(45), weight: E(70.6), name: F(&quot;Caz&quot;), male: A},
   {age: D(10), weight: E(98.5), name: F(&quot;Dan&quot;), male: B(true)},
   {age: A, weight: A, name: F(&quot;Eve&quot;), male: B(false)}];
*/

db15.re

type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
/*
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
*/

db16.re

let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));
/*
let dbCol: signatureColWise =
  {ageList: [D(18), D(25), D(45), D(10), A],
   weightList: [E(98.5), E(81.5), E(70.6), E(98.5), A],
   nameList: [F(&quot;Ada&quot;), F(&quot;Ben&quot;), F(&quot;Caz&quot;), F(&quot;Dan&quot;), F(&quot;Eve&quot;)],
   maleList: [B(false), B(true), A, B(true), B(false)]};
*/

db17.re

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
/* 
type sec =
    G(prim)
  | H(list(sec))
  | I(array(sec))
  | J((string, sec))
  | K({ key: string, value: sec, });
*/

db18.re

exception Unimplemented_type(string);
// exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};
// let secToList: sec =&gt; list(prim) = &lt;fun&gt;;

db19.re

let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};
// let trySecToList: sec =&gt; list(prim) = &lt;fun&gt;;

db2.re

let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
// let toMut: &#x27;a =&gt; mut(&#x27;a) = &lt;fun&gt;;

let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;
// let fromMut: mut(&#x27;a) =&gt; &#x27;a = &lt;fun&gt;;

db20.re

let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}
// let getCounts: list(StringMap.key) =&gt; list((string, int)) = &lt;fun&gt;;

db21.re

let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};
// let getMedian: list(float) =&gt; float = &lt;fun&gt;;

db22.re

let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));
// let getMean: list(float) =&gt; float = &lt;fun&gt;;

db23.re

type stringStats = {
  counts: list((string, int)),
};
// type stringStats = { counts: list((string, int)), };

type floatStats = {
  mean: float,
  median: float,
};
// type floatStats = { mean: float, median: float, };

db24.re

let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};
/*
let listToFloat:
  (list(prim), ~boolAllowed: bool=?, ~intAllowed: bool=?, unit) =&gt; list(float) =
  &lt;fun&gt;;
*/

db25.re

exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};
// let listToString: (list(prim), ~debug: bool=?, unit) =&gt; list(string) = &lt;fun&gt;;

db26.re

let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};
// let getFloatStats: (sec, ~level: int=?, unit) =&gt; floatStats = &lt;fun&gt;;

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}
// let getStringStats: (sec, ~debug: bool=?, unit) =&gt; stringStats = &lt;fun&gt;;

db27.re

let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));
// let primListToSec: list(prim) =&gt; sec = &lt;fun&gt;;

db28.re

let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);
/*
let ages: sec = H([G((D(18))), G((D(25))), G((D(45))), G((D(10))), G(A)]);
let weights: sec =
  H([G((E(98.5))), G((E(81.5))), G((E(70.6))), G((E(98.5))), G(A)]);
let names: sec =
  H([G((F(&quot;Ada&quot;))), G((F(&quot;Ben&quot;))), G((F(&quot;Caz&quot;))), G((F(&quot;Dan&quot;))), G((F(&quot;Eve&quot;)))]);
let males: sec =
  H([G((B(false))), G((B(true))), G(A), G((B(true))), G((B(false)))]);
*/

db29.re

getStringStats(names, ~debug=true, ());
// - : stringStats = {counts: [(&quot;Ada&quot;, 1), (&quot;Ben&quot;, 1), (&quot;Caz&quot;, 1), (&quot;Dan&quot;, 1), (&quot;Eve&quot;, 1)]}

getFloatStats(weights, ~level=1, ());
// - : floatStats = {mean: 87.275, median: 90.}

getStringStats(weights, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;70.6&quot;, 1), (&quot;81.5&quot;, 1), (&quot;98.5&quot;, 2)]}

getFloatStats(ages, ~level=2, ());
// - : floatStats = {mean: 24.5, median: 21.5}

getStringStats(ages, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;10.&quot;, 1), (&quot;18.&quot;, 1), (&quot;25.&quot;, 1), (&quot;45.&quot;, 1)]}

getFloatStats(males, ~level=3, ());
// - : floatStats = {mean: 0.5, median: 0.5}

getStringStats(males, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;0.&quot;, 2), (&quot;1.&quot;, 2)]}

db3.re

let x = ref(0); // Equivalent to let x = toMut(0);
// let x: ref(int) = {contents: 0};

x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);
// - : int = 1

db4.re

type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);
// type prim = A | B(bool) | C(char) | D(int) | E(float) | F(string);

db5.re

let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};
// let change: mut(prim) =&gt; prim = &lt;fun&gt;;

db6.re

let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};
// let toString: mut(prim) =&gt; string = &lt;fun&gt;;

db7.re

let a = toMut(A); toString(a); a.value = change(a); toString(a);
// let a: mut(prim) = {value: A};
// - : string = &quot;empty&quot;
// - : string = &quot;empty&quot;

let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
// let b: mut(prim) = {value: B(false)};
// - : string = &quot;false&quot;
// - : string = &quot;true&quot;

let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
// let c: mut(prim) = {value: C(&#x27;a&#x27;)};
// - : string = &quot;a&quot;
// - : string = &quot;b&quot;

let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
// let d: mut(prim) = {value: D(0)};
// - : string = &quot;0&quot;
// - : string = &quot;+1&quot;

let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
// let e: mut(prim) = {value: E(0.)};
// - : string = &quot;0.&quot;
// - : string = &quot;+1.&quot;

let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);
// let f: mut(prim) = {value: F(&quot;Hello&quot;)};
// - : string = &quot;Hello&quot;
// - : string = &quot;Hello!&quot;

db8.re

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];
/*
let dbRaw: list(array((string, prim))) =
  [[|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(false))|],
   [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)),
     (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)),
     (&quot;alive&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|]];

*/

db9.re

module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});
// module StringMap: { ... };</code></pre><p>Finally, transforming primitive lists to the expected input format for statistical analysis:</p><pre><code>db.re

/* HANDLING PRIMITIVE TYPES */

// Mutability in ReasonML is a feature primarily used with records. Here&#x27;s how you define a mutable type that can hold any value:
type mut(&#x27;a) = {
  mutable value: &#x27;a,
};

// In λ-calculus, function types like f: A -&gt; B imply a transformation or proof from A to B. The functions toMut and fromMut serve as bridges between mutable and immutable types, showing they can be interchangeable:
let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;

// Using the standard implementation as a reference, you can see how it translates in practical terms:
let x = ref(0); // Equivalent to let x = toMut(0);
x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);

// ReasonML requires explicit type declarations for union types, unlike TypeScript where you might use &quot;int | null&quot;:
type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);

// Variant types in ReasonML, akin to sum types or dependent types in other languages, are exhaustive and unique, ensuring no overlap between types.

// Handling these types necessitates a switch statement, covering all possible variants for completeness:
let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};

// For pattern matching, especially when not all cases are addressed explicitly, the wildcard &quot;_&quot; can be a fallback. The &quot;when&quot; keyword allows for additional conditions in matches, offering a concise way to handle complex patterns:
let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};

// Testing different cases to demonstrate how these functions work with the defined types:
let a = toMut(A); toString(a); a.value = change(a); toString(a);
let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);

/* DATABASE STORAGE FOR DATA SCIENCE */

// Working with generic types and function handling is one thing, but let&#x27;s step into a scenario where the stakes are higher: being data scientists at a medical center, tasked with deriving basic statistics from patient data. Given a raw database in a text file format, we&#x27;ve managed to extract key information as follows:

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];

// The data&#x27;s format is row-wise with an arbitrary order, which could include duplicates, missing, or extra items. To streamline debugging, we&#x27;re aiming to cast these to string maps.

// Here&#x27;s where the Map.Make functor comes into play, allowing us to generate a StringMap keyed by strings for easier readability and manipulation, akin to handling JSON objects:
module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});

// Converting our map to a JSON-like string for debug-friendliness:
let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};

// Transitioning to a generic database format, our row-wise data gets a transformation. Here, we&#x27;re all about clarity and correctness:
let showJson = true;
let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);

// Accessing the elements becomes straightforward. Missing elements? No biggie, we handle that gracefully:
let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};

// After some exploration and analysis, key insights emerge regarding age, weight, name, and gender. These form the cornerstone of our new database signature:
type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};

// Structuring a strictly-typed database while ensuring all necessary keys are included and defaults are set for missing items:
let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);

// Finally, the database is correctly formatted. Next up, transposing this database to a column-wise format, ready for statistical analysis:
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};

// Successfully transposing our data, we&#x27;re set to dive deep into the analysis, equipped with a database that&#x27;s both comprehensive and accurately structured.
let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));

/* STATISTICS LIBRARY DEVELOPMENT */

// Venturing into building a generic statistics library, we&#x27;re focusing on versatility across different data structures. Whether dealing with Lists or Arrays, the goal is seamless integration and handling.

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
  
// The challenge lies in unpacking these varied structures into a consistent format, ideally a list of primitives, for statistical analysis. Given the evolving nature of our library, not all types are fully supported yet, leading to potential exceptions for unhandled cases.
exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};

// To ensure a smooth user experience, we wrap secToList in a function that gracefully handles exceptions, providing clear feedback rather than abrupt errors.
let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};

// Diving into the core of our library, we aim to offer basic but essential statistical functions, each designed to work with a specific type of data.

// getCounts tackles enumeration, mapping each unique string in a list to its frequency of occurrence, ideal for categorical data analysis.
let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}

// getMedian finds the middle value in a list of floats after sorting, a key measure of central tendency for quantitative data.
let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};

// getMean computes the average from a list of floats, providing a quick snapshot of your data&#x27;s central value.
let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));

// Structuring our output, we define types for summarizing string and float data, encapsulating counts for categorical data and central measures for continuous data.
type stringStats = {
  counts: list((string, int)),
};

type floatStats = {
  mean: float,
  median: float,
};

/* DATA ANALYSIS FRAMEWORK */

// Integrating complex data structures into actionable insights requires a systematic approach. We&#x27;ve established methods to deconstruct complex data into primitive lists and have statistical functions ready. The challenge now is to seamlessly connect these components.

// First, let&#x27;s categorize data types based on their analytical utility:

// - Nominal data, like colors &quot;Blue&quot; and &quot;Yellow&quot;, are distinct without a meaningful order. The mode serves as their central tendency measure.
// - Boolean data, a subset of nominal, consists of binary choices like &quot;Yes&quot; and &quot;No&quot;.
// - Ordinal data, such as ratings from 1 (&quot;Low&quot;) to 5 (&quot;High&quot;), imply order but not the uniformity of scale. Their median reflects central tendency.
// - Numeric data, representing continuous or interval data, can be fully quantified. The mean is used to express their central tendency.

// Recognizing that not all operations apply universally across data types underscores the importance of targeted analytical strategies.

// Transitioning to the implementation phase:

// The `listToFloat` function converts a list of primitives to floats, selectively allowing boolean and integer conversions based on flags:
let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};

// Converting primitives to strings while handling incompatible types by casting to floats, then stringifying, allows for flexible data interpretation:
exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};

// `getFloatStats` and `getStringStats` functions then process these lists into statistical summaries, considering the data level restrictions and debug options respectively:
let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}

// Finally, transforming primitive lists to the expected input format for statistical analysis:
let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));

// Extracting statistics becomes straightforward with prepped data:
let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);

// Now, it&#x27;s just a matter of calling the appropriate statistical function for each data type, with optional debugging for string conversions:
getStringStats(names, ~debug=true, ());
getFloatStats(weights, ~level=1, ());
getStringStats(weights, ~debug=true, ());

getFloatStats(ages, ~level=2, ());
getStringStats(ages, ~debug=true, ());

getFloatStats(males, ~level=3, ());
getStringStats(males, ~debug=true, ());

db1.re

type mut(&#x27;a) = {
  mutable value: &#x27;a,
};
// type mut(&#x27;a) = { mutable value: &#x27;a, };

db10.re

let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};
// let mapToJson: StringMap.t(prim) =&gt; string = &lt;fun&gt;;

db11.re

let showJson = true;
// let showJson: bool = true;

let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);
/* let dbGeneric: list(StringMap.t(prim)) =
  [&lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;];
*/
/*
{age: +18, male: false, name: Ada, weight: +98.5}
{age: +25, male: true, name: Ben, weight: +81.5}
{age: +45, alive: true, name: Caz, weight: +70.6}
{age: +10, male: true, name: Dan, weight: +98.5}
{male: false, name: Eve}
*/

db12.re

let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};
// let tryAccessDbGeneric: (StringMap.key, int) =&gt; prim = &lt;fun&gt;;

db13.re

type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};
// type signature = { age: prim, weight: prim, name: prim, male: prim, };

db14.re

let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);
/*
let db: list(signature) =
  [{age: D(18), weight: E(98.5), name: F(&quot;Ada&quot;), male: B(false)},
   {age: D(25), weight: E(81.5), name: F(&quot;Ben&quot;), male: B(true)},
   {age: D(45), weight: E(70.6), name: F(&quot;Caz&quot;), male: A},
   {age: D(10), weight: E(98.5), name: F(&quot;Dan&quot;), male: B(true)},
   {age: A, weight: A, name: F(&quot;Eve&quot;), male: B(false)}];
*/

db15.re

type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
/*
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
*/

db16.re

let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));
/*
let dbCol: signatureColWise =
  {ageList: [D(18), D(25), D(45), D(10), A],
   weightList: [E(98.5), E(81.5), E(70.6), E(98.5), A],
   nameList: [F(&quot;Ada&quot;), F(&quot;Ben&quot;), F(&quot;Caz&quot;), F(&quot;Dan&quot;), F(&quot;Eve&quot;)],
   maleList: [B(false), B(true), A, B(true), B(false)]};
*/

db17.re

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
/* 
type sec =
    G(prim)
  | H(list(sec))
  | I(array(sec))
  | J((string, sec))
  | K({ key: string, value: sec, });
*/

db18.re

exception Unimplemented_type(string);
// exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};
// let secToList: sec =&gt; list(prim) = &lt;fun&gt;;

db19.re

let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};
// let trySecToList: sec =&gt; list(prim) = &lt;fun&gt;;

db2.re

let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
// let toMut: &#x27;a =&gt; mut(&#x27;a) = &lt;fun&gt;;

let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;
// let fromMut: mut(&#x27;a) =&gt; &#x27;a = &lt;fun&gt;;

db20.re

let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}
// let getCounts: list(StringMap.key) =&gt; list((string, int)) = &lt;fun&gt;;

db21.re

let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};
// let getMedian: list(float) =&gt; float = &lt;fun&gt;;

db22.re

let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));
// let getMean: list(float) =&gt; float = &lt;fun&gt;;

db23.re

type stringStats = {
  counts: list((string, int)),
};
// type stringStats = { counts: list((string, int)), };

type floatStats = {
  mean: float,
  median: float,
};
// type floatStats = { mean: float, median: float, };

db24.re

let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};
/*
let listToFloat:
  (list(prim), ~boolAllowed: bool=?, ~intAllowed: bool=?, unit) =&gt; list(float) =
  &lt;fun&gt;;
*/

db25.re

exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};
// let listToString: (list(prim), ~debug: bool=?, unit) =&gt; list(string) = &lt;fun&gt;;

db26.re

let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};
// let getFloatStats: (sec, ~level: int=?, unit) =&gt; floatStats = &lt;fun&gt;;

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}
// let getStringStats: (sec, ~debug: bool=?, unit) =&gt; stringStats = &lt;fun&gt;;

db27.re

let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));
// let primListToSec: list(prim) =&gt; sec = &lt;fun&gt;;

db28.re

let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);
/*
let ages: sec = H([G((D(18))), G((D(25))), G((D(45))), G((D(10))), G(A)]);
let weights: sec =
  H([G((E(98.5))), G((E(81.5))), G((E(70.6))), G((E(98.5))), G(A)]);
let names: sec =
  H([G((F(&quot;Ada&quot;))), G((F(&quot;Ben&quot;))), G((F(&quot;Caz&quot;))), G((F(&quot;Dan&quot;))), G((F(&quot;Eve&quot;)))]);
let males: sec =
  H([G((B(false))), G((B(true))), G(A), G((B(true))), G((B(false)))]);
*/

db29.re

getStringStats(names, ~debug=true, ());
// - : stringStats = {counts: [(&quot;Ada&quot;, 1), (&quot;Ben&quot;, 1), (&quot;Caz&quot;, 1), (&quot;Dan&quot;, 1), (&quot;Eve&quot;, 1)]}

getFloatStats(weights, ~level=1, ());
// - : floatStats = {mean: 87.275, median: 90.}

getStringStats(weights, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;70.6&quot;, 1), (&quot;81.5&quot;, 1), (&quot;98.5&quot;, 2)]}

getFloatStats(ages, ~level=2, ());
// - : floatStats = {mean: 24.5, median: 21.5}

getStringStats(ages, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;10.&quot;, 1), (&quot;18.&quot;, 1), (&quot;25.&quot;, 1), (&quot;45.&quot;, 1)]}

getFloatStats(males, ~level=3, ());
// - : floatStats = {mean: 0.5, median: 0.5}

getStringStats(males, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;0.&quot;, 2), (&quot;1.&quot;, 2)]}

db3.re

let x = ref(0); // Equivalent to let x = toMut(0);
// let x: ref(int) = {contents: 0};

x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);
// - : int = 1

db4.re

type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);
// type prim = A | B(bool) | C(char) | D(int) | E(float) | F(string);

db5.re

let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};
// let change: mut(prim) =&gt; prim = &lt;fun&gt;;

db6.re

let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};
// let toString: mut(prim) =&gt; string = &lt;fun&gt;;

db7.re

let a = toMut(A); toString(a); a.value = change(a); toString(a);
// let a: mut(prim) = {value: A};
// - : string = &quot;empty&quot;
// - : string = &quot;empty&quot;

let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
// let b: mut(prim) = {value: B(false)};
// - : string = &quot;false&quot;
// - : string = &quot;true&quot;

let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
// let c: mut(prim) = {value: C(&#x27;a&#x27;)};
// - : string = &quot;a&quot;
// - : string = &quot;b&quot;

let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
// let d: mut(prim) = {value: D(0)};
// - : string = &quot;0&quot;
// - : string = &quot;+1&quot;

let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
// let e: mut(prim) = {value: E(0.)};
// - : string = &quot;0.&quot;
// - : string = &quot;+1.&quot;

let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);
// let f: mut(prim) = {value: F(&quot;Hello&quot;)};
// - : string = &quot;Hello&quot;
// - : string = &quot;Hello!&quot;

db8.re

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];
/*
let dbRaw: list(array((string, prim))) =
  [[|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(false))|],
   [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)),
     (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)),
     (&quot;alive&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|]];

*/

db9.re

module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});
// module StringMap: { ... };</code></pre><p>Extracting statistics becomes straightforward with prepped data:</p><pre><code>db.re

/* HANDLING PRIMITIVE TYPES */

// Mutability in ReasonML is a feature primarily used with records. Here&#x27;s how you define a mutable type that can hold any value:
type mut(&#x27;a) = {
  mutable value: &#x27;a,
};

// In λ-calculus, function types like f: A -&gt; B imply a transformation or proof from A to B. The functions toMut and fromMut serve as bridges between mutable and immutable types, showing they can be interchangeable:
let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;

// Using the standard implementation as a reference, you can see how it translates in practical terms:
let x = ref(0); // Equivalent to let x = toMut(0);
x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);

// ReasonML requires explicit type declarations for union types, unlike TypeScript where you might use &quot;int | null&quot;:
type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);

// Variant types in ReasonML, akin to sum types or dependent types in other languages, are exhaustive and unique, ensuring no overlap between types.

// Handling these types necessitates a switch statement, covering all possible variants for completeness:
let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};

// For pattern matching, especially when not all cases are addressed explicitly, the wildcard &quot;_&quot; can be a fallback. The &quot;when&quot; keyword allows for additional conditions in matches, offering a concise way to handle complex patterns:
let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};

// Testing different cases to demonstrate how these functions work with the defined types:
let a = toMut(A); toString(a); a.value = change(a); toString(a);
let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);

/* DATABASE STORAGE FOR DATA SCIENCE */

// Working with generic types and function handling is one thing, but let&#x27;s step into a scenario where the stakes are higher: being data scientists at a medical center, tasked with deriving basic statistics from patient data. Given a raw database in a text file format, we&#x27;ve managed to extract key information as follows:

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];

// The data&#x27;s format is row-wise with an arbitrary order, which could include duplicates, missing, or extra items. To streamline debugging, we&#x27;re aiming to cast these to string maps.

// Here&#x27;s where the Map.Make functor comes into play, allowing us to generate a StringMap keyed by strings for easier readability and manipulation, akin to handling JSON objects:
module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});

// Converting our map to a JSON-like string for debug-friendliness:
let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};

// Transitioning to a generic database format, our row-wise data gets a transformation. Here, we&#x27;re all about clarity and correctness:
let showJson = true;
let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);

// Accessing the elements becomes straightforward. Missing elements? No biggie, we handle that gracefully:
let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};

// After some exploration and analysis, key insights emerge regarding age, weight, name, and gender. These form the cornerstone of our new database signature:
type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};

// Structuring a strictly-typed database while ensuring all necessary keys are included and defaults are set for missing items:
let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);

// Finally, the database is correctly formatted. Next up, transposing this database to a column-wise format, ready for statistical analysis:
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};

// Successfully transposing our data, we&#x27;re set to dive deep into the analysis, equipped with a database that&#x27;s both comprehensive and accurately structured.
let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));

/* STATISTICS LIBRARY DEVELOPMENT */

// Venturing into building a generic statistics library, we&#x27;re focusing on versatility across different data structures. Whether dealing with Lists or Arrays, the goal is seamless integration and handling.

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
  
// The challenge lies in unpacking these varied structures into a consistent format, ideally a list of primitives, for statistical analysis. Given the evolving nature of our library, not all types are fully supported yet, leading to potential exceptions for unhandled cases.
exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};

// To ensure a smooth user experience, we wrap secToList in a function that gracefully handles exceptions, providing clear feedback rather than abrupt errors.
let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};

// Diving into the core of our library, we aim to offer basic but essential statistical functions, each designed to work with a specific type of data.

// getCounts tackles enumeration, mapping each unique string in a list to its frequency of occurrence, ideal for categorical data analysis.
let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}

// getMedian finds the middle value in a list of floats after sorting, a key measure of central tendency for quantitative data.
let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};

// getMean computes the average from a list of floats, providing a quick snapshot of your data&#x27;s central value.
let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));

// Structuring our output, we define types for summarizing string and float data, encapsulating counts for categorical data and central measures for continuous data.
type stringStats = {
  counts: list((string, int)),
};

type floatStats = {
  mean: float,
  median: float,
};

/* DATA ANALYSIS FRAMEWORK */

// Integrating complex data structures into actionable insights requires a systematic approach. We&#x27;ve established methods to deconstruct complex data into primitive lists and have statistical functions ready. The challenge now is to seamlessly connect these components.

// First, let&#x27;s categorize data types based on their analytical utility:

// - Nominal data, like colors &quot;Blue&quot; and &quot;Yellow&quot;, are distinct without a meaningful order. The mode serves as their central tendency measure.
// - Boolean data, a subset of nominal, consists of binary choices like &quot;Yes&quot; and &quot;No&quot;.
// - Ordinal data, such as ratings from 1 (&quot;Low&quot;) to 5 (&quot;High&quot;), imply order but not the uniformity of scale. Their median reflects central tendency.
// - Numeric data, representing continuous or interval data, can be fully quantified. The mean is used to express their central tendency.

// Recognizing that not all operations apply universally across data types underscores the importance of targeted analytical strategies.

// Transitioning to the implementation phase:

// The `listToFloat` function converts a list of primitives to floats, selectively allowing boolean and integer conversions based on flags:
let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};

// Converting primitives to strings while handling incompatible types by casting to floats, then stringifying, allows for flexible data interpretation:
exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};

// `getFloatStats` and `getStringStats` functions then process these lists into statistical summaries, considering the data level restrictions and debug options respectively:
let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}

// Finally, transforming primitive lists to the expected input format for statistical analysis:
let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));

// Extracting statistics becomes straightforward with prepped data:
let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);

// Now, it&#x27;s just a matter of calling the appropriate statistical function for each data type, with optional debugging for string conversions:
getStringStats(names, ~debug=true, ());
getFloatStats(weights, ~level=1, ());
getStringStats(weights, ~debug=true, ());

getFloatStats(ages, ~level=2, ());
getStringStats(ages, ~debug=true, ());

getFloatStats(males, ~level=3, ());
getStringStats(males, ~debug=true, ());

db1.re

type mut(&#x27;a) = {
  mutable value: &#x27;a,
};
// type mut(&#x27;a) = { mutable value: &#x27;a, };

db10.re

let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};
// let mapToJson: StringMap.t(prim) =&gt; string = &lt;fun&gt;;

db11.re

let showJson = true;
// let showJson: bool = true;

let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);
/* let dbGeneric: list(StringMap.t(prim)) =
  [&lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;];
*/
/*
{age: +18, male: false, name: Ada, weight: +98.5}
{age: +25, male: true, name: Ben, weight: +81.5}
{age: +45, alive: true, name: Caz, weight: +70.6}
{age: +10, male: true, name: Dan, weight: +98.5}
{male: false, name: Eve}
*/

db12.re

let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};
// let tryAccessDbGeneric: (StringMap.key, int) =&gt; prim = &lt;fun&gt;;

db13.re

type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};
// type signature = { age: prim, weight: prim, name: prim, male: prim, };

db14.re

let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);
/*
let db: list(signature) =
  [{age: D(18), weight: E(98.5), name: F(&quot;Ada&quot;), male: B(false)},
   {age: D(25), weight: E(81.5), name: F(&quot;Ben&quot;), male: B(true)},
   {age: D(45), weight: E(70.6), name: F(&quot;Caz&quot;), male: A},
   {age: D(10), weight: E(98.5), name: F(&quot;Dan&quot;), male: B(true)},
   {age: A, weight: A, name: F(&quot;Eve&quot;), male: B(false)}];
*/

db15.re

type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
/*
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
*/

db16.re

let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));
/*
let dbCol: signatureColWise =
  {ageList: [D(18), D(25), D(45), D(10), A],
   weightList: [E(98.5), E(81.5), E(70.6), E(98.5), A],
   nameList: [F(&quot;Ada&quot;), F(&quot;Ben&quot;), F(&quot;Caz&quot;), F(&quot;Dan&quot;), F(&quot;Eve&quot;)],
   maleList: [B(false), B(true), A, B(true), B(false)]};
*/

db17.re

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
/* 
type sec =
    G(prim)
  | H(list(sec))
  | I(array(sec))
  | J((string, sec))
  | K({ key: string, value: sec, });
*/

db18.re

exception Unimplemented_type(string);
// exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};
// let secToList: sec =&gt; list(prim) = &lt;fun&gt;;

db19.re

let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};
// let trySecToList: sec =&gt; list(prim) = &lt;fun&gt;;

db2.re

let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
// let toMut: &#x27;a =&gt; mut(&#x27;a) = &lt;fun&gt;;

let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;
// let fromMut: mut(&#x27;a) =&gt; &#x27;a = &lt;fun&gt;;

db20.re

let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}
// let getCounts: list(StringMap.key) =&gt; list((string, int)) = &lt;fun&gt;;

db21.re

let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};
// let getMedian: list(float) =&gt; float = &lt;fun&gt;;

db22.re

let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));
// let getMean: list(float) =&gt; float = &lt;fun&gt;;

db23.re

type stringStats = {
  counts: list((string, int)),
};
// type stringStats = { counts: list((string, int)), };

type floatStats = {
  mean: float,
  median: float,
};
// type floatStats = { mean: float, median: float, };

db24.re

let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};
/*
let listToFloat:
  (list(prim), ~boolAllowed: bool=?, ~intAllowed: bool=?, unit) =&gt; list(float) =
  &lt;fun&gt;;
*/

db25.re

exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};
// let listToString: (list(prim), ~debug: bool=?, unit) =&gt; list(string) = &lt;fun&gt;;

db26.re

let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};
// let getFloatStats: (sec, ~level: int=?, unit) =&gt; floatStats = &lt;fun&gt;;

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}
// let getStringStats: (sec, ~debug: bool=?, unit) =&gt; stringStats = &lt;fun&gt;;

db27.re

let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));
// let primListToSec: list(prim) =&gt; sec = &lt;fun&gt;;

db28.re

let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);
/*
let ages: sec = H([G((D(18))), G((D(25))), G((D(45))), G((D(10))), G(A)]);
let weights: sec =
  H([G((E(98.5))), G((E(81.5))), G((E(70.6))), G((E(98.5))), G(A)]);
let names: sec =
  H([G((F(&quot;Ada&quot;))), G((F(&quot;Ben&quot;))), G((F(&quot;Caz&quot;))), G((F(&quot;Dan&quot;))), G((F(&quot;Eve&quot;)))]);
let males: sec =
  H([G((B(false))), G((B(true))), G(A), G((B(true))), G((B(false)))]);
*/

db29.re

getStringStats(names, ~debug=true, ());
// - : stringStats = {counts: [(&quot;Ada&quot;, 1), (&quot;Ben&quot;, 1), (&quot;Caz&quot;, 1), (&quot;Dan&quot;, 1), (&quot;Eve&quot;, 1)]}

getFloatStats(weights, ~level=1, ());
// - : floatStats = {mean: 87.275, median: 90.}

getStringStats(weights, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;70.6&quot;, 1), (&quot;81.5&quot;, 1), (&quot;98.5&quot;, 2)]}

getFloatStats(ages, ~level=2, ());
// - : floatStats = {mean: 24.5, median: 21.5}

getStringStats(ages, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;10.&quot;, 1), (&quot;18.&quot;, 1), (&quot;25.&quot;, 1), (&quot;45.&quot;, 1)]}

getFloatStats(males, ~level=3, ());
// - : floatStats = {mean: 0.5, median: 0.5}

getStringStats(males, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;0.&quot;, 2), (&quot;1.&quot;, 2)]}

db3.re

let x = ref(0); // Equivalent to let x = toMut(0);
// let x: ref(int) = {contents: 0};

x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);
// - : int = 1

db4.re

type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);
// type prim = A | B(bool) | C(char) | D(int) | E(float) | F(string);

db5.re

let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};
// let change: mut(prim) =&gt; prim = &lt;fun&gt;;

db6.re

let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};
// let toString: mut(prim) =&gt; string = &lt;fun&gt;;

db7.re

let a = toMut(A); toString(a); a.value = change(a); toString(a);
// let a: mut(prim) = {value: A};
// - : string = &quot;empty&quot;
// - : string = &quot;empty&quot;

let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
// let b: mut(prim) = {value: B(false)};
// - : string = &quot;false&quot;
// - : string = &quot;true&quot;

let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
// let c: mut(prim) = {value: C(&#x27;a&#x27;)};
// - : string = &quot;a&quot;
// - : string = &quot;b&quot;

let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
// let d: mut(prim) = {value: D(0)};
// - : string = &quot;0&quot;
// - : string = &quot;+1&quot;

let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
// let e: mut(prim) = {value: E(0.)};
// - : string = &quot;0.&quot;
// - : string = &quot;+1.&quot;

let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);
// let f: mut(prim) = {value: F(&quot;Hello&quot;)};
// - : string = &quot;Hello&quot;
// - : string = &quot;Hello!&quot;

db8.re

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];
/*
let dbRaw: list(array((string, prim))) =
  [[|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(false))|],
   [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)),
     (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)),
     (&quot;alive&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|]];

*/

db9.re

module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});
// module StringMap: { ... };</code></pre><p>Now, it’s just a matter of calling the appropriate statistical function for each data type, with optional debugging for string conversions:</p><pre><code>db.re

/* HANDLING PRIMITIVE TYPES */

// Mutability in ReasonML is a feature primarily used with records. Here&#x27;s how you define a mutable type that can hold any value:
type mut(&#x27;a) = {
  mutable value: &#x27;a,
};

// In λ-calculus, function types like f: A -&gt; B imply a transformation or proof from A to B. The functions toMut and fromMut serve as bridges between mutable and immutable types, showing they can be interchangeable:
let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;

// Using the standard implementation as a reference, you can see how it translates in practical terms:
let x = ref(0); // Equivalent to let x = toMut(0);
x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);

// ReasonML requires explicit type declarations for union types, unlike TypeScript where you might use &quot;int | null&quot;:
type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);

// Variant types in ReasonML, akin to sum types or dependent types in other languages, are exhaustive and unique, ensuring no overlap between types.

// Handling these types necessitates a switch statement, covering all possible variants for completeness:
let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};

// For pattern matching, especially when not all cases are addressed explicitly, the wildcard &quot;_&quot; can be a fallback. The &quot;when&quot; keyword allows for additional conditions in matches, offering a concise way to handle complex patterns:
let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};

// Testing different cases to demonstrate how these functions work with the defined types:
let a = toMut(A); toString(a); a.value = change(a); toString(a);
let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);

/* DATABASE STORAGE FOR DATA SCIENCE */

// Working with generic types and function handling is one thing, but let&#x27;s step into a scenario where the stakes are higher: being data scientists at a medical center, tasked with deriving basic statistics from patient data. Given a raw database in a text file format, we&#x27;ve managed to extract key information as follows:

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];

// The data&#x27;s format is row-wise with an arbitrary order, which could include duplicates, missing, or extra items. To streamline debugging, we&#x27;re aiming to cast these to string maps.

// Here&#x27;s where the Map.Make functor comes into play, allowing us to generate a StringMap keyed by strings for easier readability and manipulation, akin to handling JSON objects:
module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});

// Converting our map to a JSON-like string for debug-friendliness:
let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};

// Transitioning to a generic database format, our row-wise data gets a transformation. Here, we&#x27;re all about clarity and correctness:
let showJson = true;
let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);

// Accessing the elements becomes straightforward. Missing elements? No biggie, we handle that gracefully:
let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};

// After some exploration and analysis, key insights emerge regarding age, weight, name, and gender. These form the cornerstone of our new database signature:
type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};

// Structuring a strictly-typed database while ensuring all necessary keys are included and defaults are set for missing items:
let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);

// Finally, the database is correctly formatted. Next up, transposing this database to a column-wise format, ready for statistical analysis:
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};

// Successfully transposing our data, we&#x27;re set to dive deep into the analysis, equipped with a database that&#x27;s both comprehensive and accurately structured.
let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));

/* STATISTICS LIBRARY DEVELOPMENT */

// Venturing into building a generic statistics library, we&#x27;re focusing on versatility across different data structures. Whether dealing with Lists or Arrays, the goal is seamless integration and handling.

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
  
// The challenge lies in unpacking these varied structures into a consistent format, ideally a list of primitives, for statistical analysis. Given the evolving nature of our library, not all types are fully supported yet, leading to potential exceptions for unhandled cases.
exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};

// To ensure a smooth user experience, we wrap secToList in a function that gracefully handles exceptions, providing clear feedback rather than abrupt errors.
let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};

// Diving into the core of our library, we aim to offer basic but essential statistical functions, each designed to work with a specific type of data.

// getCounts tackles enumeration, mapping each unique string in a list to its frequency of occurrence, ideal for categorical data analysis.
let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}

// getMedian finds the middle value in a list of floats after sorting, a key measure of central tendency for quantitative data.
let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};

// getMean computes the average from a list of floats, providing a quick snapshot of your data&#x27;s central value.
let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));

// Structuring our output, we define types for summarizing string and float data, encapsulating counts for categorical data and central measures for continuous data.
type stringStats = {
  counts: list((string, int)),
};

type floatStats = {
  mean: float,
  median: float,
};

/* DATA ANALYSIS FRAMEWORK */

// Integrating complex data structures into actionable insights requires a systematic approach. We&#x27;ve established methods to deconstruct complex data into primitive lists and have statistical functions ready. The challenge now is to seamlessly connect these components.

// First, let&#x27;s categorize data types based on their analytical utility:

// - Nominal data, like colors &quot;Blue&quot; and &quot;Yellow&quot;, are distinct without a meaningful order. The mode serves as their central tendency measure.
// - Boolean data, a subset of nominal, consists of binary choices like &quot;Yes&quot; and &quot;No&quot;.
// - Ordinal data, such as ratings from 1 (&quot;Low&quot;) to 5 (&quot;High&quot;), imply order but not the uniformity of scale. Their median reflects central tendency.
// - Numeric data, representing continuous or interval data, can be fully quantified. The mean is used to express their central tendency.

// Recognizing that not all operations apply universally across data types underscores the importance of targeted analytical strategies.

// Transitioning to the implementation phase:

// The `listToFloat` function converts a list of primitives to floats, selectively allowing boolean and integer conversions based on flags:
let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};

// Converting primitives to strings while handling incompatible types by casting to floats, then stringifying, allows for flexible data interpretation:
exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};

// `getFloatStats` and `getStringStats` functions then process these lists into statistical summaries, considering the data level restrictions and debug options respectively:
let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}

// Finally, transforming primitive lists to the expected input format for statistical analysis:
let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));

// Extracting statistics becomes straightforward with prepped data:
let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);

// Now, it&#x27;s just a matter of calling the appropriate statistical function for each data type, with optional debugging for string conversions:
getStringStats(names, ~debug=true, ());
getFloatStats(weights, ~level=1, ());
getStringStats(weights, ~debug=true, ());

getFloatStats(ages, ~level=2, ());
getStringStats(ages, ~debug=true, ());

getFloatStats(males, ~level=3, ());
getStringStats(males, ~debug=true, ());

db1.re

type mut(&#x27;a) = {
  mutable value: &#x27;a,
};
// type mut(&#x27;a) = { mutable value: &#x27;a, };

db10.re

let mapToJson = map =&gt; {
  &quot;{&quot; ++ StringMap.fold((k, v, acc) =&gt; {
    let strV = toString(toMut(v));
    let item = k ++ &quot;: &quot; ++ strV;
    acc == &quot;&quot; ? item : acc ++ &quot;, &quot; ++ item;
  }, map, &quot;&quot;) ++ &quot;}&quot;;
};
// let mapToJson: StringMap.t(prim) =&gt; string = &lt;fun&gt;;

db11.re

let showJson = true;
// let showJson: bool = true;

let dbGeneric = List.map(row =&gt; {
  let map = ref(StringMap.empty);
  Array.to_list(row) |&gt; List.iter(((k, v)) =&gt; {
    map := StringMap.add(k, v, map^);
  });
  if (showJson) print_endline(mapToJson(map^));
  map^;
}, dbRaw);
/* let dbGeneric: list(StringMap.t(prim)) =
  [&lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;, &lt;abstr&gt;];
*/
/*
{age: +18, male: false, name: Ada, weight: +98.5}
{age: +25, male: true, name: Ben, weight: +81.5}
{age: +45, alive: true, name: Caz, weight: +70.6}
{age: +10, male: true, name: Dan, weight: +98.5}
{male: false, name: Eve}
*/

db12.re

let tryAccessDbGeneric = (key, i) =&gt; {
  try(StringMap.find(key, List.nth(dbGeneric, i))) {
    | Not_found =&gt; { print_endline(&quot;Not found, defaulting to A&quot;); A; }
  };
};
// let tryAccessDbGeneric: (StringMap.key, int) =&gt; prim = &lt;fun&gt;;

db13.re

type signature = {
  age: prim,
  weight: prim,
  name: prim,
  male: prim,
};
// type signature = { age: prim, weight: prim, name: prim, male: prim, };

db14.re

let db = List.map(row =&gt; {
  let record = ref({age: A, name: A, weight: A, male: A});
  List.iter(((k, v)) =&gt; {
    switch (k) { 
    | &quot;age&quot; =&gt; (record := {...record^, age: v}) 
    | &quot;name&quot; =&gt; (record := {...record^, name: v}) 
    | &quot;weight&quot; =&gt; (record := {...record^, weight: v}) 
    | &quot;male&quot; =&gt; (record := {...record^, male: v}) 
    | _ =&gt; ()
    };
  }, Array.to_list(row));
  record^;
}, dbRaw);
/*
let db: list(signature) =
  [{age: D(18), weight: E(98.5), name: F(&quot;Ada&quot;), male: B(false)},
   {age: D(25), weight: E(81.5), name: F(&quot;Ben&quot;), male: B(true)},
   {age: D(45), weight: E(70.6), name: F(&quot;Caz&quot;), male: A},
   {age: D(10), weight: E(98.5), name: F(&quot;Dan&quot;), male: B(true)},
   {age: A, weight: A, name: F(&quot;Eve&quot;), male: B(false)}];
*/

db15.re

type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
/*
type signatureColWise = {
  mutable ageList: list(prim),
  mutable weightList: list(prim),
  mutable nameList: list(prim),
  mutable maleList: list(prim),
};
*/

db16.re

let dbCol = List.(fold_left((acc, row) =&gt; {
  acc.ageList = concat([acc.ageList, [row.age]]);
  acc.weightList = concat([acc.weightList, [row.weight]]);
  acc.nameList = concat([acc.nameList, [row.name]]);
  acc.maleList = concat([acc.maleList, [row.male]]);
  acc;
}, {ageList: [], weightList: [], nameList: [], maleList: []}, db));
/*
let dbCol: signatureColWise =
  {ageList: [D(18), D(25), D(45), D(10), A],
   weightList: [E(98.5), E(81.5), E(70.6), E(98.5), A],
   nameList: [F(&quot;Ada&quot;), F(&quot;Ben&quot;), F(&quot;Caz&quot;), F(&quot;Dan&quot;), F(&quot;Eve&quot;)],
   maleList: [B(false), B(true), A, B(true), B(false)]};
*/

db17.re

type sec = 
  | G(prim) // Base type for primitives
  | H(list(sec)) // Iterable collections like lists
  | I(array(sec)) // Iterable collections like arrays
  | J((string, sec)) // Complex types involving key-value pairs
  | K({key: string, value: sec}); // Record types with named fields
/* 
type sec =
    G(prim)
  | H(list(sec))
  | I(array(sec))
  | J((string, sec))
  | K({ key: string, value: sec, });
*/

db18.re

exception Unimplemented_type(string);
// exception Unimplemented_type(string);

let secToList = values =&gt; {
  let iterable = switch (values) {
  | H(items) =&gt; items
  | I(items) =&gt; Array.to_list(items)
  | J((key, _)) | K({key, _}) =&gt; raise(Unimplemented_type(&quot;Complex structures not supported: &quot; ++ key))
  | G(_) =&gt; raise(Invalid_argument(&quot;Expected an iterable, received a primitive&quot;))
  };

  let listPrims = List.map(item =&gt; {
    switch (item) {
    | G(value) =&gt; value
    | _ =&gt; A // Fallback for unhandled cases
    }
  }, iterable);
  
  listPrims;
};
// let secToList: sec =&gt; list(prim) = &lt;fun&gt;;

db19.re

let trySecToList = values =&gt; {
  try (secToList(values)) {
  | Invalid_argument(msg) | Unimplemented_type(msg) =&gt; { print_endline(msg); []; }
  };
};
// let trySecToList: sec =&gt; list(prim) = &lt;fun&gt;;

db2.re

let toMut: &#x27;a =&gt; mut(&#x27;a) = value =&gt; {value: value};
// let toMut: &#x27;a =&gt; mut(&#x27;a) = &lt;fun&gt;;

let fromMut: mut(&#x27;a) =&gt; &#x27;a = ({value}) =&gt; value;
// let fromMut: mut(&#x27;a) =&gt; &#x27;a = &lt;fun&gt;;

db20.re

let getCounts = items =&gt; {
  let map = ref(StringMap.empty);
  List.iter(item =&gt; {
    map := StringMap.update(item, (value) =&gt; {
      switch (value) {
      | Some(count) =&gt; Some(count + 1)
      | None =&gt; Some(1)
      };
    }, map^);
  }, items);
  let counts = ref([]);
  StringMap.iter((k, v) =&gt; {
    counts := List.append(counts^, [(k ++ &quot;&quot;, v)]);
  }, map^);
  let countsSorted = List.sort(((_, a), (_, b)) =&gt; a - b, counts^);
  countsSorted;
}
// let getCounts: list(StringMap.key) =&gt; list((string, int)) = &lt;fun&gt;;

db21.re

let getMedian = items =&gt; {
  let sorted = List.sort((a, b) =&gt; compare(a, b), items);
  let len = List.length(sorted);
  if (len mod 2 == 1) List.nth(sorted, len / 2) else (List.nth(sorted, len / 2 - 1) +. List.nth(sorted, len / 2)) /. 2.;
};
// let getMedian: list(float) =&gt; float = &lt;fun&gt;;

db22.re

let getMean = items =&gt; List.fold_left((+.), 0., items) /. float_of_int(List.length(items));
// let getMean: list(float) =&gt; float = &lt;fun&gt;;

db23.re

type stringStats = {
  counts: list((string, int)),
};
// type stringStats = { counts: list((string, int)), };

type floatStats = {
  mean: float,
  median: float,
};
// type floatStats = { mean: float, median: float, };

db24.re

let listToFloat = (listPrims, ~boolAllowed as allowB = false, ~intAllowed as allowI = allowB, ()) =&gt; {
  List.filter_map(item =&gt; {
    switch (item) {
    | B(flag) when flag &amp;&amp; allowB =&gt; Some(0.)
    | B(flag) when !flag &amp;&amp; allowB =&gt; Some(1.) 
    | D(number) when allowI =&gt; Some(float_of_int(number))
    | E(number) =&gt; Some(number)
    | _ =&gt; None
    }
  }, listPrims);
};
/*
let listToFloat:
  (list(prim), ~boolAllowed: bool=?, ~intAllowed: bool=?, unit) =&gt; list(float) =
  &lt;fun&gt;;
*/

db25.re

exception Incompatible_string;
let listToString = (listPrims, ~debug: option(bool) = ?, ()) =&gt; {  
  try (List.map(item =&gt; {
    switch (item) {
    | F(word) =&gt; word
    | _ =&gt; raise(Incompatible_string)
    }
  }, listPrims)) {
    | Incompatible_string =&gt; { 
      switch (debug) {
        | Some(flag) when flag =&gt; { print_endline(&quot;Converting to float ...&quot;); }
        | _ =&gt; ()
      }; 
      listPrims
        |&gt; listToFloat(_, ~boolAllowed=true, ())
        |&gt; List.map(num =&gt; string_of_float(num));
    }
  };
};
// let listToString: (list(prim), ~debug: bool=?, unit) =&gt; list(string) = &lt;fun&gt;;

db26.re

let getFloatStats = (l, ~level=0, ()) =&gt; {
  let allows = Array.init(3, i =&gt; i &lt;= level);

  let floatStats = l
    |&gt; trySecToList
    |&gt; listToFloat(_, ~boolAllowed=allows[2], ~intAllowed=allows[1], ())
    |&gt; (l =&gt; {
        median: getMedian(l),
        mean: getMean(l),
      });
   
   floatStats;
};
// let getFloatStats: (sec, ~level: int=?, unit) =&gt; floatStats = &lt;fun&gt;;

let getStringStats = (l, ~debug: option(bool) = ?, ()) =&gt; {  
  let stringStats = l
    |&gt; trySecToList
    |&gt; listToString(_, ~debug=?debug, ())
    |&gt; (l =&gt; {
      counts: getCounts(l),
    });
    
  stringStats;
}
// let getStringStats: (sec, ~debug: bool=?, unit) =&gt; stringStats = &lt;fun&gt;;

db27.re

let primListToSec = primList =&gt; H(List.map(item =&gt; G(item), primList));
// let primListToSec: list(prim) =&gt; sec = &lt;fun&gt;;

db28.re

let (ages, weights, names, males) = (
  primListToSec(dbCol.ageList), 
  primListToSec(dbCol.weightList), 
  primListToSec(dbCol.nameList),
  primListToSec(dbCol.maleList)
);
/*
let ages: sec = H([G((D(18))), G((D(25))), G((D(45))), G((D(10))), G(A)]);
let weights: sec =
  H([G((E(98.5))), G((E(81.5))), G((E(70.6))), G((E(98.5))), G(A)]);
let names: sec =
  H([G((F(&quot;Ada&quot;))), G((F(&quot;Ben&quot;))), G((F(&quot;Caz&quot;))), G((F(&quot;Dan&quot;))), G((F(&quot;Eve&quot;)))]);
let males: sec =
  H([G((B(false))), G((B(true))), G(A), G((B(true))), G((B(false)))]);
*/

db29.re

getStringStats(names, ~debug=true, ());
// - : stringStats = {counts: [(&quot;Ada&quot;, 1), (&quot;Ben&quot;, 1), (&quot;Caz&quot;, 1), (&quot;Dan&quot;, 1), (&quot;Eve&quot;, 1)]}

getFloatStats(weights, ~level=1, ());
// - : floatStats = {mean: 87.275, median: 90.}

getStringStats(weights, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;70.6&quot;, 1), (&quot;81.5&quot;, 1), (&quot;98.5&quot;, 2)]}

getFloatStats(ages, ~level=2, ());
// - : floatStats = {mean: 24.5, median: 21.5}

getStringStats(ages, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;10.&quot;, 1), (&quot;18.&quot;, 1), (&quot;25.&quot;, 1), (&quot;45.&quot;, 1)]}

getFloatStats(males, ~level=3, ());
// - : floatStats = {mean: 0.5, median: 0.5}

getStringStats(males, ~debug=true, ());
// Converting to float ...
// - : stringStats = {counts: [(&quot;0.&quot;, 2), (&quot;1.&quot;, 2)]}

db3.re

let x = ref(0); // Equivalent to let x = toMut(0);
// let x: ref(int) = {contents: 0};

x := x^ + 1; // This increments x, similar to x.value = x.value + 1;
x^; // Extracts the value from x, just like fromMut(x);
// - : int = 1

db4.re

type prim = 
  | A 
  | B(bool) 
  | C(char) 
  | D(int) 
  | E(float) 
  | F(string);
// type prim = A | B(bool) | C(char) | D(int) | E(float) | F(string);

db5.re

let change = (ptr: mut(prim)) =&gt; {
  switch (ptr.value) {
  | A =&gt; A
  | B(flag) =&gt; B(!flag)
  | C(letter) =&gt; C(Char.chr(Char.code(letter) + 1))
  | D(number) =&gt; D(number + 1)
  | E(number) =&gt; E(number +. 1.)
  | F(word) =&gt; F(word ++ &quot;!&quot;)
  };
};
// let change: mut(prim) =&gt; prim = &lt;fun&gt;;

db6.re

let toString = ({ value }) =&gt; {
  switch (value) {
  | A =&gt; &quot;empty&quot;
  | B(flag) =&gt; Bool.to_string(flag)
  | C(letter) =&gt; Char.escaped(letter)
  | D(0) =&gt; &quot;0&quot;
  | D(pos) when pos &gt; 0 =&gt; &quot;+&quot; ++ Int.to_string(pos)
  | D(neg) when neg &lt; 0 =&gt; Int.to_string(neg)
  | E(0.) =&gt; &quot;0.&quot;
  | E(pos) when pos &gt; 0. =&gt; &quot;+&quot; ++ Float.to_string(pos)
  | E(neg) when neg &lt; 0. =&gt; Float.to_string(neg)
  | F(word) =&gt; word
  | _ =&gt; &quot;other&quot;
  }
};
// let toString: mut(prim) =&gt; string = &lt;fun&gt;;

db7.re

let a = toMut(A); toString(a); a.value = change(a); toString(a);
// let a: mut(prim) = {value: A};
// - : string = &quot;empty&quot;
// - : string = &quot;empty&quot;

let b = toMut(B(false)); toString(b); b.value = change(b); toString(b);
// let b: mut(prim) = {value: B(false)};
// - : string = &quot;false&quot;
// - : string = &quot;true&quot;

let c = toMut(C(&#x27;a&#x27;)); toString(c); c.value = change(c); toString(c);
// let c: mut(prim) = {value: C(&#x27;a&#x27;)};
// - : string = &quot;a&quot;
// - : string = &quot;b&quot;

let d = toMut(D(0)); toString(d); d.value = change(d); toString(d);
// let d: mut(prim) = {value: D(0)};
// - : string = &quot;0&quot;
// - : string = &quot;+1&quot;

let e = toMut(E(0.)); toString(e); e.value = change(e); toString(e);
// let e: mut(prim) = {value: E(0.)};
// - : string = &quot;0.&quot;
// - : string = &quot;+1.&quot;

let f = toMut(F(&quot;Hello&quot;)); toString(f); f.value = change(f); toString(f);
// let f: mut(prim) = {value: F(&quot;Hello&quot;)};
// - : string = &quot;Hello&quot;
// - : string = &quot;Hello!&quot;

db8.re

let dbRaw = [
  [|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(false))|],
  [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)), (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)), (&quot;alive&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)), (&quot;male&quot;, B(true))|],
  [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|],
];
/*
let dbRaw: list(array((string, prim))) =
  [[|(&quot;age&quot;, D(18)), (&quot;name&quot;, F(&quot;Ada&quot;)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(false))|],
   [|(&quot;age&quot;, D(25)), (&quot;weight&quot;, E(81.5)), (&quot;name&quot;, F(&quot;Bon&quot;)),
     (&quot;name&quot;, F(&quot;Ben&quot;)), (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Caz&quot;)), (&quot;weight&quot;, E(70.6)), (&quot;age&quot;, D(45)),
     (&quot;alive&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Dan&quot;)), (&quot;age&quot;, D(10)), (&quot;weight&quot;, E(98.5)),
     (&quot;male&quot;, B(true))|],
   [|(&quot;name&quot;, F(&quot;Eve&quot;)), (&quot;male&quot;, B(false))|]];

*/

db9.re

module StringMap = Map.Make({
  type t = string;
  let compare = compare;
});
// module StringMap: { ... };</code></pre><p>Wrapping up our deep dive into handling a database use case with ReasonML, it’s clear we’ve covered significant ground. From extracting raw data to applying a generic statistics library, this journey showcased ReasonML’s capability to tackle complex data challenges head-on.</p><p>I hope you enjoyed reading my article series. Stay tuned!</p>
{% endraw %}
