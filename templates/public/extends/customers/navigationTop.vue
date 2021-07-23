<v-app-bar
    style="background: linear-gradient(to right, #7C4DFF, #304FFE, #448AFF);;"
    absolute
    dark
    dense
>

  {% include 'public/extends/customers/appBar.vue' %}

  <v-app-bar-title>Mango BOT</v-app-bar-title>

  <v-switch
      style="margin-top: 25px; margin-left: 15px"
      v-model="$vuetify.theme.dark"
      inset
      label="Change Theme Dark"
  ></v-switch>

  <v-spacer></v-spacer>
  <div :hidden="!loaderSpin">
    <v-progress-circular
        :width="3"
        color="green accent-1"
        indeterminate
    ></v-progress-circular>
  </div>

  <div :hidden="!loaderData">
    [[userAuth.name]]
    &nbsp;
    <v-menu
        bottom
        left
        transition="slide-y-transition"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
            icon
            v-bind="attrs"
            v-on="on"
        >
          <v-avatar>
            <img
                :loading="!spinAuth"
                :src="[[userAuth.picture]]"
                alt="John"
            >
          </v-avatar>
        </v-btn>
      </template>

      <v-list>
        <v-list-item @click="isProfile = true">
          <v-card
              class="mx-auto"
              max-width="434"
              tile
          >
            <v-avatar
                class="profile"
                color="grey"
                size="250"
                tile
            >
              <v-img :src="userAuth.picture">
                <v-row
                    align="end"
                    class="fill-height"
                >
                  <v-col
                      align-self="start"
                      class="pa-0"
                      cols="12"
                  >
                  </v-col>
                  <v-col class="py-0">
                    <v-list-item
                        color="rgba(0, 0, 0, .4)"
                        dark
                    >
                      <v-list-item-content>
                        <v-list-item-title class="text-h6">
                          [[userAuth.name]]
                        </v-list-item-title>
                        <v-list-item-subtitle>Email: [[userAuth.email]]</v-list-item-subtitle>
                        <v-spacer></v-spacer>
                        <v-btn text color="red" @click="logout">
                          <strong>Logout</strong>
                        </v-btn>
                      </v-list-item-content>
                    </v-list-item>
                  </v-col>
                </v-row>
              </v-img>
            </v-avatar>
          </v-card>
        </v-list-item>
      </v-list>
    </v-menu>
    &nbsp;&nbsp;
  </div>
</v-app-bar>