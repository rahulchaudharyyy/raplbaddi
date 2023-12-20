<template>
  <GMapAutocomplete
    placeholder="This is a placeholder"
    @place_changed="setPlace"
  >
  </GMapAutocomplete>
</template>
<script>
export default {
  name: 'App',
  data() {
    return {};
  },
  methods: {
    setPlace(e) {
      console.log(e);
    },
  },
};
</script>