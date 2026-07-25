module.exports = {
  daemon: true,
  run: [
    {
      method: "local.set",
      params: {
        port: "{{port}}"
      }
    },
    {
      method: "shell.run",
      params: {
        env: {
          FRONTEND_PORT: "{{local.port}}"
        },
        path: "app",
        // Pinokio's conda env puts GNU tar first in PATH, which cannot extract the
        // backend zip archives ("Cannot connect to C: resolve failed"). Prepend
        // System32 in the same command so serve.cjs resolves the Windows bsdtar
        // (each message array entry runs in its own shell, so it must be one chain).
        message: "{{platform === 'win32' ? 'set \"PATH=%SystemRoot%\\\\System32;%PATH%\" && ' + path.join('app', 'tools', 'node-win', 'node.exe') : platform === 'darwin' ? './app/tools/node-mac/bin/node' : './app/tools/node-linux/bin/node'}} scripts/server/serve.cjs",
        on: [{
          event: "/backend.*ready/i",
          done: true
        }]
      }
    },
    {
      method: "local.set",
      params: {
        url: "http://localhost:{{local.port}}"
      }
    }
  ]
}
