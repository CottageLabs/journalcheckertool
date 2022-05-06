let st = undefined;
let ft = document.getElementById('funder');
_ready = () => {
  ft = document.getElementById('funder');
  if (ft !== null) {
    clearInterval(st);
  }
}
if (ft === null) st = setInterval(_ready,100);