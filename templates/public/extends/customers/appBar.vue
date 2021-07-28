<v-menu
    bottom
    left
    transition="slide-y-transition"
>
  <template v-slot:activator="{ on, attrs }">
    <v-app-bar-nav-icon
        v-bind="attrs"
        v-on="on"
    ></v-app-bar-nav-icon>
  </template>

  <v-list>
    <v-list-item @click="navigatorAppbar = true">
      <v-list shaped>
        <v-subheader>Menu Pages</v-subheader>
        <v-list-item-group
            v-model="selectedList"
            color="pink lighten-2"
        >
          <v-list-item
              v-for="(item, i) in itemsAppbar"
              :key="i"
              @click="redirectPage(item)"
          >
              <v-list-item-icon>
                <v-icon v-text="item.icon"></v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title v-text="item.text"></v-list-item-title>
              </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-list-item>
  </v-list>

</v-menu>