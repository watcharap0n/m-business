{% extends "admin/main_layout.html" %}
{% block content %}

<br>
<br>
<div id="app">
    <v-app id="inspire">
        <!-- contents -->
    </v-app>
</div>


<script>

    new Vue({
        el: '#app' ,
        vuetify: new Vuetify(),
        data: {}
    })


</script>




{% endblock %}