public class hexagono implements calculable {
  public double calcularArea() {
    double lado = 10;
    double calculo = (3*Math.pow(lado, 2)*(Math.sqrt(3)/2));
    System.out.println(calculo);
    return calculo;
  }
}