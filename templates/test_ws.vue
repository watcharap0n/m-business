{% extends "admin/main_layout.html" %}
{% block content %}

  <br>
  <br>
  <div class="text-center">
    <h2 @click="sendMessage('Webscoket')">Hello Websocket</h2>

    <h2 @click="sendMessage('Model')">Hello Model</h2>

    <h2 @click="sendMessage('View')">Hello View</h2>

    <div :hidden="!status">
      [[message]]
    </div>


  </div>


  {% block script %}
    <script src="/static/js/ws.js"></script>
  {% endblock %}

{% endblock %}