
//  gsap.from(".line h1",{
// y:150,
// stagger:0.3,
// duration:0.3,
//  delay:0.1, 
// }) 


// var t1 = gsap.timeline()
// t1.to("#loader",{
// opacity:0,
// duration:0.3,
// delay:2
//  })

// t1.to("#loader",{
//   display:"none"
// })

/* filter in products*/
document.addEventListener("DOMContentLoaded", function () {
  const priceSlider = document.getElementById("price-slider");
  const minInput = document.getElementById("min_price");
  const maxInput = document.getElementById("max_price");
  const minDisplay = document.getElementById("min_price_display");
  const maxDisplay = document.getElementById("max_price_display");

  if (priceSlider && minInput && maxInput && minDisplay && maxDisplay) {
    const minValue = parseInt(minInput.value || 0);
    const maxValue = parseInt(maxInput.value || 1000000);

    noUiSlider.create(priceSlider, {
      start: [minValue, maxValue],
      connect: true,
      step: 100,
      range: {
        min: 0,
        max: 1000000,
      },
      format: {
        to: value => Math.round(value),
        from: value => Number(value)
      }
    });

    // Slider → Input
    priceSlider.noUiSlider.on("update", function (values) {
      const [minVal, maxVal] = values;
      minInput.value = minVal;
      maxInput.value = maxVal;
      minDisplay.value = minVal;
      maxDisplay.value = maxVal;
    });

    // Input → Slider (on blur or Enter)
    minDisplay.addEventListener("change", function () {
      let val = parseInt(this.value) || 0;
      let currentMax = parseInt(maxDisplay.value) || 1000000;
      priceSlider.noUiSlider.set([val, currentMax]);
    });

    maxDisplay.addEventListener("change", function () {
      let val = parseInt(this.value) || 100000;
      let currentMin = parseInt(minDisplay.value) || 0;
      priceSlider.noUiSlider.set([currentMin, val]);
    });
  }
});

// for product details
function changeImage(event, src) {
  document.getElementById("mainImage").src = src;

  }