// ShopZone app.js

// === Flash auto-dismiss ===
document.querySelectorAll('.flash').forEach(function(el) {
  setTimeout(function() {
    el.style.opacity = '0';
    el.style.transition = 'opacity 0.5s';
    setTimeout(function() { el.remove(); }, 500);
  }, 4000);
});

// === Password toggle ===
function togglePwd(inputId, btn) {
  var input = document.getElementById(inputId);
  if (!input) return;
  if (input.type === 'password') {
    input.type = 'text';
    btn.textContent = '\uD83D\uDE48';
  } else {
    input.type = 'password';
    btn.textContent = '\uD83D\uDC41';
  }
}

// === Product page qty +/- ===
function adjQty(delta) {
  var input = document.getElementById('qty-input');
  if (!input) return;
  var val = parseInt(input.value) + delta;
  if (val < 1) val = 1;
  if (val > 99) val = 99;
  input.value = val;
}

// === Cart page qty +/- bound to a form ===
function adjForm(btn, delta) {
  var form = btn.closest('.ci-qty-form');
  if (!form) return;
  var input = form.querySelector('input[name="quantity"]');
  if (!input) return;
  var val = parseInt(input.value) + delta;
  if (val < 1) val = 1;
  if (val > 99) val = 99;
  input.value = val;
  form.submit();
}

// === Session timeout warning ===
(function() {
  var warned = false;
  setTimeout(function() {
    if (!warned) {
      warned = true;
      if (document.querySelector('.nav-dropdown')) {
        var d = document.createElement('div');
        d.className = 'flash flash-warning';
        d.style.cssText = 'position:fixed;bottom:20px;right:20px;z-index:9999;animation:slideIn .3s ease';
        d.innerHTML = '<span>\u23F1 Your session will expire in 2 minutes.</span>' +
          '<button class="flash-close" onclick="this.parentElement.remove()">\u00D7</button>';
        document.body.appendChild(d);
        setTimeout(function() { d.remove(); }, 8000);
      }
    }
  }, 28 * 60 * 1000);
})();
