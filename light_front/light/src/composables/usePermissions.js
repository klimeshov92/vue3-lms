import { reactive } from 'vue'
import axios from 'axios'
import { baseUrl, isTokenValid } from '../utils/utils'

const state = reactive({
  loaded: false,

  // 🔁 имена как в компонентах
  //permissionsVersion: null,
  globalPermissionsList: [],
  objectPermissionsDict: {},
})

let intervalId = null

async function loadPermissions(force = false) {
  let token = localStorage.getItem('access_token')
  const validToken = isTokenValid(token)

  if (token && !validToken) {
    localStorage.removeItem('access_token')
    localStorage.removeItem('userPermissions')
    token = null
  }

  const cached = JSON.parse(localStorage.getItem('userPermissions'))

  if (cached && !force) {
    state.globalPermissionsList = cached.global_permissions || []
    state.objectPermissionsDict = cached.object_permissions || {}
    //state.permissionsVersion = cached.permissions_version || null
    state.loaded = true
    return
  }

  const resp = await axios.get(`${baseUrl}/user_permissions/`, {
    headers: {
      ...(token && { Authorization: `Bearer ${token}` }),
    },
  })

  localStorage.setItem('userPermissions', JSON.stringify(resp.data))

  state.globalPermissionsList = resp.data.global_permissions || []
  state.objectPermissionsDict = resp.data.object_permissions || {}
  //state.permissionsVersion = resp.data.permissions_version || null
  state.loaded = true
}

async function checkPermissionsVersion() {
  //if (!state.permissionsVersion) return

  let token = localStorage.getItem('access_token')
  const validToken = isTokenValid(token)

  if (!token || !validToken) return

  //const resp = await axios.get(`${baseUrl}/user_permissions_version/`, {
  //  headers: {
  //    Authorization: `Bearer ${token}`,
  //  },
  //})

  //if (resp.data.permissions_version !== state.permissionsVersion) {
  //  await loadPermissions(true)
  //}
}

function startWatcher() {
  if (intervalId) return
  intervalId = setInterval(checkPermissionsVersion, 60000)
}

function stopWatcher() {
  if (intervalId) {
    clearInterval(intervalId)
    intervalId = null
  }
}

export function usePermissions() {
  return {
    state,
    loadPermissions,
    startWatcher,
    stopWatcher,
  }
}
