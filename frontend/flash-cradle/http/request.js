import axios from 'axios'

// const baseUrl = 
//   process.env.NODE_ENV === 'development'
//     ? "http://101.200.29.174:30000"// dev
//     : "http://101.200.29.174:30000" // pro

const service = axios.create({
  baseURL: '',
  timeout: 10000
})

export default service