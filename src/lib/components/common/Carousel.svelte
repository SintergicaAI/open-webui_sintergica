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
    <button class="arrow prev" on:click={prevSlide}>↑</button>
    <button class="arrow next" on:click={nextSlide}>↓</button>
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
    margin: 0 auto;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .slides {
    display: flex;
    flex-direction: column; /* Cambia de un carrusel horizontal a uno vertical */
    height: 100vh; /* Tamaño para ajustarse a toda la pantalla */
    transition: transform 0.5s ease-in-out;
    transform: translateY(calc(-100% * var(--currentSlide))); /* Control deslizante vertical */
  }

  .slide {
    min-height: 100%;
    width: 100%; /* Ocupa todo el ancho */
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
  }

  /* Ajustar las flechas */
  .arrow {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
  }

  .arrow.prev {
    top: 10px; /* Mover hacia la parte superior */
  }

  .arrow.next {
    bottom: 10px; /* Mover hacia la parte inferior */
  }

  .dots {
    position: absolute;
    top: 50%;
    right: 10px;
    transform: translateX(-50%);
    display: flex;
    flex-direction: column;
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