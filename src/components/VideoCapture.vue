<template>
  <div class="video-capture">
    <h3 class="title is-3">Video Cpature</h3>
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
      <button
        type="submit"
        class="button is-link"
        :disabled="capturedData.data == null"
        @click="uploadCapturedVideo"
      >
        アップロード
      </button>
    </div>
  </div>
</template>

<script>
/* eslint-disable-next-line import/no-extraneous-dependencies */
import { mapState } from 'vuex'

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
 *
 * @vue-prop {String} user
 *
 *   User ID to work with. `kikuo` by default.
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
    },
    user: {
      type: String,
      default: 'kikuo'
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
  computed: {
    ...mapState(['apiBaseUrl']),
    // Upload destination URL
    uploadUrl () {
      return `${this.apiBaseUrl}/video/${this.user}`
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
    uploadCapturedVideo () {
      console.log('uploading video')
      const body = new Blob(
        [this.capturedData.data],
        { type: 'application/octet-stream' }
      )
      fetch(
        this.uploadUrl,
        {
          method: 'POST',
          body
        }
      )
        .then(response => {
          console.log(response)
          response.text()
            .then(text => console.log(text))
        })
        .catch(err => console.log(err))
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
        // TODO: should be .mkv?
        //       anyway, .mkv did not work but .webm did with OSX + Chrome
        return '.webm'
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
        autoGainControl: true,
        // NOTE: no need for echo canceller
        //       because audio playback is suppressed
        echoCancellation: false,
        noiseSuppression: true
      }
    }
    navigator.mediaDevices.getUserMedia(streamConstraints)
      .then(stream => {
        console.log('capture started')
        this.isDeviceReady = true
        this.stream = stream
        // starts playback of captured video
        // excludes audio tracks from the playback to avoid echoes
        const playbackStream = new MediaStream(stream.getVideoTracks())
        /* eslint-disable-next-line prefer-destructuring */
        const video = this.$refs.video
        video.srcObject = playbackStream
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
