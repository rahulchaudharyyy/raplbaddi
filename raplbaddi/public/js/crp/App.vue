<script setup>
import { ref } from "vue";

const dynamicMessage = ref("Hello from App.vue");
</script>
<template>
  <div>
	<h3>{{ dynamicMessage }}</h3>
    <h4>Start editing at raplbaddi/public/js/crp/App.vue</h4>
  </div>
</template>