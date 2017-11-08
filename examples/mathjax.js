// From github.com/fsavje/math-with-slack

// Add Mathjax source
addDependency("https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.2/MathJax.js");
// Add Mathjax config
$('head').append($('<script />', {type:'text/x-mathjax-config', text: `
  MathJax.Hub.Config({
    messageStyle: 'none',
    extensions: ['tex2jax.js'],
    jax: ['input/TeX', 'output/HTML-CSS'],
    tex2jax: {
      displayMath: [['$$', '$$']],
      element: 'msgs_div',
      ignoreClass: 'ql-editor',
      inlineMath: [['$', '$']],
      processEscapes: true,
      skipTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
    },
    TeX: {
      extensions: ['AMSmath.js', 'AMSsymbols.js', 'noErrors.js', 'noUndefined.js']
    }
  });
`}));

var options = { attributes: false, childList: true, characterData: true, subtree: true };
var observer = new MutationObserver(function (r, o) {
  MathJax.Hub.Queue(['Typeset', MathJax.Hub]);
});
observer.observe($("#msgs_div")[0], options);