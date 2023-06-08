
<script>
    setInterval(function() {
        fetch('/autCallf/')
            .then(response => response.text())
            .then(data => console.log(data))
            .catch(error => console.error(error))
    }, 1000); // 120000 milliseconds = 2 minutes
</script>
