<template>
  <div class="video-capture">
    <h1 class="title is-1">Video Cpature</h1>
    <div>
      <div
        class="video-container"
        :style="videoContainerStyle"
      >
        <video ref="video" class="video" :width="width">
        </video>
      </div>
      <button
        class="button is-primary"
        @click="startRecording"
        :disabled="!isDeviceReady"
      >
        録画
      </button>
      <a
        v-show="capturedData.data !== null"
        :href="capturedData.objectUrl"
        :download="capturedData.fileName"
      >
        保存
      </a>
    </div>
  </div>
</template>

<script>
/**
 * Video Capture.
 *
 * @vue-prop {Number} width
 *
 *   Width, in pixels, of the video frame.
 *   `400` by default.
 *
 * @vue-prop {Number} recordingTimeInMs
 *
 *   Recording time respresented in milliseconds.
 *   `5000`; i.e., 5 seconds by default.
 *
 * @vue-prop {Number} timesliceInMs
 *
 *   Duration, in milliseconds, of each chunk in a video stream.
 *   `1000`; i.e., 1 second by default.
 *
 *   NOTE: Does not matter on Safari as of 2019-07-08.
 */
export default {
  name: 'video-capture',
  props: {
    width: {
      type: Number,
      default: 400
    },
    recordingTimeInMs: {
      type: Number,
      default: 5000
    },
    timesliceInMs: {
      type: Number,
      default: 1000
    }
  },
  data () {
    return {
      // turns to true when the video device becomes ready
      isDeviceReady: false,
      // video stream object
      stream: null,
      // whether recording is active
      isRecording: false,
      // information about the captured video
      capturedData: {
        // Blob of the captured video
        data: null,
        // URL of the captured video
        objectUrl: '',
        // file name of the captured video
        fileName: ''
      }
    }
  },
  methods: {
    // Starts recording captured video.
    startRecording () {
      if (this.stream !== null) {
        const recorder = new MediaRecorder(this.stream)
        const chunks = []
        recorder.ondataavailable = event => {
          console.log(`retrieved new chunk: ${event.data.type}`)
          chunks.push(event.data)
        }
        recorder.onstart = () => {
          // NOTE: does not happen on Safari as of 2019-07-08
          console.log('recording started')
        }
        recorder.onstop = () => {
          console.log('recording stopped')
          if (chunks.length === 0) {
            console.log('no video recorded')
            this.isRecording = false
            return
          }
          // concatenates retrieved Blob chunks
          // NOTE: Blob constructor does not respect chunks' type
          //       so the mime type needs to be retrieved from
          //       one of recorded chunks
          const mimeType = chunks[0].type
          console.log(`mime type: ${mimeType}`)
          this.capturedData.data = new Blob(chunks, {
            type: mimeType
          })
          this.capturedData.objectUrl = URL.createObjectURL(
            this.capturedData.data
          )
          const extension = this.getExtensionOfMimeType(mimeType)
          this.capturedData.fileName = `my-video${extension}`
          console.log(`file name: ${this.capturedData.fileName}`)
          this.isRecording = false
        }
        recorder.start(this.timesliceInMs)
        this.isRecording = true
        setTimeout(
          () => {
            recorder.stop()
          },
          this.recordingTimeInMs
        )
      }
    },
    // Returns the file extension corresponding to a given mime-type.
    // Returns an empty string if there is no known extension for mimeType.
    getExtensionOfMimeType (mimeType) {
      if (mimeType.startsWith('video/mp4')) {
        return '.mp4'
      }
      if (mimeType.startsWith('video/webm')) {
        return '.webm'
      }
      if (mimeType.startsWith('video/x-matroska')) {
        return '.mkv'
      }
      // default
      return ''
    }
  },
  mounted () {
    console.log('VideoCapture.vue: mounted')
    // starts capturing video
    const streamConstraints = {
      video: true,
      audio: {
        echoCancellation: true,
        noiseSuppression: true
      }
    }
    navigator.mediaDevices.getUserMedia(streamConstraints)
      .then(stream => {
        console.log('capture started')
        this.isDeviceReady = true
        this.stream = stream
        // starts playback of captured video
        /* eslint-disable-next-line prefer-destructuring */
        const video = this.$refs.video
        video.srcObject = stream
        video.play()
      })
      .catch(err => {
        console.log(err)
      })
  },
  beforeDestroy () {
    /* eslint-disable-next-line prefer-destructuring */
    const video = this.$refs.video
    video.pause()
  }
}
</script>

<style>
.video-capture {
  text-align: center;
}
</style>
