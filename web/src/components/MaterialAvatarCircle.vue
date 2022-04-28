<template>
  <div :class="sizeStyle().out">
    <div :class="sizeStyle().in">
      <v-img :src="image" cover></v-img>
      <h2>
        {{ title }} <br />
        <span>{{ content }}</span>
      </h2>
      <a :href="url">{{ textBtn }}</a>
    </div>
  </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue'
export default defineComponent({
  name: 'MaterialAvatarCircle',
  props: {
    size: String,
    image: {
      type: String,
      default: 'tom.jpg'
    },
    title: {
      type: String,
      default: 'Need help?'
    },
    content: {
      type: String,
      default: 'Ping this guy'
    },
    textBtn: {
      type: String,
      default: 'Ping him'
    },
    url: {
      type: String,
      default: '#'
    }
  },
  setup(props) {
    function sizeStyle() {
      var value = { out: 'box', in: 'content' }
      if (String(props.size).toLowerCase() === 'small') {
        value = { out: 'box-small', in: 'content-small' }
      }
      return value
    }
    return {
      sizeStyle
    }
  }
})
</script>
<style lang="scss" scoped>
.box {
  position: relative;
  width: 300px;
  height: 300px;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  overflow: hidden;
}
.box::before {
  content: '';
  position: absolute;
  inset: -10px 110px;
  background: linear-gradient(315deg, #00ccff, #d400d4);
  transition: 0.5s;
  animation: animate 4s linear infinite;
}
.box:hover::before,
.box-small:hover::before {
  inset: -20px 0px;
}
@keyframes animate {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
.box::after,
.box-small::after {
  content: '';
  position: absolute;
  inset: 6px;
  background: transparent;
  //   background: #162052;
  border-radius: 50%;
  z-index: 1;
}
.content {
  position: absolute;
  inset: 10px;
  //   border: 6px solid #070a1c;
  border: 6px solid rgba(7, 10, 28, 0.7);
  z-index: 3;
  border-radius: 50%;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}
.content .v-img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transform: 0.5s;
  pointer-events: none;
  z-index: 3;
}
.box:hover .content .v-img {
  opacity: 0;
}
.content h2 {
  position: relative;
  font-size: 1.5em;
  text-align: center;
  color: #fff;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}
.content h2 span {
  font-weight: 300;
  font-size: 0.75em;
}
.content a {
  position: relative;
  margin-top: 10px;
  padding: 10px 20px;
  background: #fff;
  color: #070a1c;
  border-radius: 25px;
  font-weight: 500;
  font-size: 1.25em;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  text-decoration: none;
  transition: 0.5s;
}
.content a:hover {
  letter-spacing: 0.2em;
}

//small part
.box-small {
  position: relative;
  width: 128px;
  height: 128px;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  overflow: hidden;
}
.box-small::before {
  content: '';
  position: absolute;
  inset: -10px 40px;
  background: linear-gradient(315deg, #00ccff, #d400d4);
  //   background: linear-gradient(315deg, #132e07, #f2a202);
  transition: 0.5s;
  animation: animate 4s linear infinite;
}
.box-small:hover .content-small .v-img {
  opacity: 0;
}
.content-small {
  position: absolute;
  inset: 3px;
  border: 3px solid rgba(7, 10, 28, 0.7);
  z-index: 3;
  border-radius: 50%;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}
.content-small .v-img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transform: 0.5s;
  pointer-events: none;
  z-index: 3;
}
.content-small h2 {
  position: relative;
  font-size: 0.75em;
  text-align: center;
  color: #fff;
  font-weight: 400;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}
.content-small h2 span {
  font-weight: 300;
  font-size: 0.7em;
}
.content-small a {
  position: relative;
  margin-top: 10px;
  padding: 5px 10px;
  background: #fff;
  color: #070a1c;
  border-radius: 25px;
  font-weight: 300;
  font-size: 0.7em;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  text-decoration: none;
  transition: 0.5s;
}
.content-small a:hover {
  letter-spacing: 0.2em;
}
</style>
