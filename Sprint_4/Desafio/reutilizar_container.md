Sim, é possível reutilizar containers em Docker, embora o funcionamento deles dependa do estado em que se encontram e das alterações realizadas neles.
Quando um container é executado e finaliza a tarefa (ou é parado), ele entra em um estado chamado "exited". Nessa situação, você pode reutilizá-lo facilmente.

``` docker
docker start <container_id>
```