<template>
  <div class="container">
    <header>
      <h1>JobForm — Envio de Currículo</h1>
    </header>

    <main>
      <JobForm />
    </main>

    <footer>
      <small>JobForm</small>
    </footer>
  </div>
</template>

<script>
  import JobForm from './components/JobForm.vue'
  export default {
    name: 'App',
    components: { JobForm }
  }
</script>

<style scoped>
  .container {
    max-width: 720px;
    margin: 24px auto;
    padding: 16px;
    font-family: system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
  }
  header h1 { margin: 0 0 8px 0 }
</style>