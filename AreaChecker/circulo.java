public class circulo implements calculable{
  public double calcularArea() {
    double medida = 5;
    double calculo = (3.14*(Math.pow(medida, 2))); 
    System.out.println(calculo);
    return calculo;
  }
}