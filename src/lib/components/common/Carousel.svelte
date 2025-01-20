<script>
  export let slides = [];
  export let autoplay = true;
  export let interval = 3000;
  export let showDots = true;
  export let showArrows = true;

  let currentSlide = 0;
  let autoSlide;

  function prevSlide() {
    currentSlide = (currentSlide - 1 + slides.length) % slides.length;
  }

  function nextSlide() {
    currentSlide = (currentSlide + 1) % slides.length;
  }

  // Funciones para manejar autoplay
  function startAutoplay() {
    stopAutoplay();
    if (autoplay) {
      autoSlide = setInterval(nextSlide, interval);
    }
  }

  function stopAutoplay() {
    if (autoSlide) clearInterval(autoSlide);
  }

  // Iniciar autoplay cuando el componente esté montado
  import { onMount, onDestroy } from 'svelte';

  onMount(() => {
    startAutoplay();
  });

  onDestroy(() => {
    stopAutoplay();
  });
</script>

<div
  class="carousel"
  on:mouseenter={stopAutoplay}
  on:mouseleave={startAutoplay}
>
  <!-- Contenedor para las diapositivas -->
  <div class="slides" style="--currentSlide: {currentSlide}">
    {#each slides as slide, i}
      <div class="slide" style="background-image: url('{slide}')"></div>
    {/each}
  </div>

  <!-- Flechas de navegación -->
  {#if showArrows}
    <button class="arrow prev" on:click={prevSlide}>&lt;</button>
    <button class="arrow next" on:click={nextSlide}>&gt;</button>
  {/if}

  <!-- Dots para navegar entre diapositivas -->
  {#if showDots}
    <div class="dots">
      {#each slides as _, i}
        <span
          class:dots__dot-active={i === currentSlide}
          on:click={() => (currentSlide = i)}
        ></span>
      {/each}
    </div>
  {/if}
</div>

<style>
  .carousel {
    position: relative;
    width: 100%;
    max-width: 800px;
    margin: 0 auto;
    overflow: hidden;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .slides {
    display: flex;
    transition: transform 0.5s ease-in-out;
    transform: translateX(calc(-100% * var(--currentSlide)));
  }

  .slide {
    min-width: 100%;
    height: 400px;
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
  }

  /* Flechas de navegación */
  .arrow {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    z-index: 10;
    background-color: rgba(0, 0, 0, 0.5);
    color: white;
    border: none;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    cursor: pointer;
    font-size: 1.5rem;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .arrow.prev {
    left: 15px;
  }

  .arrow.next {
    right: 15px;
  }

  .arrow:hover {
    background-color: rgba(0, 0, 0, 0.7);
  }

  /* Indicadores (dots) */
  .dots {
    position: absolute;
    bottom: 15px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    gap: 10px;
    z-index: 10;
  }

  .dots span {
    width: 10px;
    height: 10px;
    background-color: rgba(255, 255, 255, 0.5);
    border-radius: 50%;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  .dots span.dots__dot-active {
    background-color: rgba(255, 255, 255, 0.9);
  }
</style>