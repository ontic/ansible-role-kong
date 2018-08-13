# Documentation

## Note

I need to follow up on this [issue](https://github.com/Kong/getkong.org/issues/617) and push for changes which
would allow idempotency when running this role. Until then the custom module and documentation will remain incomplete.

Idempotency has been finally achieved since Kong is now properly supporting `PUT` HTTP methods on most API endpoints.
However I was only able to achieve this by specifying an `id` for each module which then gets converted to a UUID.

See the available modules in the `library` directory for complete documentation and examples. Currently I can easily
configure and secure the Kong Admin API, but I am considering refactoring the code base to support managing Kong with
a dictionary structured something like below.

## Example

```
kong_admin_api:
  admin_url: 'http://localhost:8001'
  admin_username:
  admin_password:
  services:
    - id: 'example-service'
      name: 'example-service'
      url: 'http://mockbin.org/request'
      state: 'present'
      routes:
        - id: 'example-public-route'
          paths: '/public'
          state: 'present'
        - id: 'example-private-route'
          paths: '/private'
          state: 'present'
          plugins:
            - id: 'example-plugin-key-auth-private-path'
              name: 'key-auth'
              enabled: true
              state: 'present'
  consumers:
    - id: 'example-consumer'
      username: 'adam'
      custom_id: '1234'
      state: 'present'
  plugins:
    - id: 'example-plugin-rate-limiting'
      name: 'rate-limiting'
      enabled: true
      state: 'present'
      config:
        minute: 5
        limit_by: 'consumer'
        policy: 'redis'
        redis_host: '127.0.0.1'
        redis_port: '6379'
        redis_password: 'secret'
        redis_timeout: '2000'
        redis_database: '0'
```

## Role Variables

Available variables are listed below, along with default values (see [defaults/main.yml](/defaults/main.yml)):

