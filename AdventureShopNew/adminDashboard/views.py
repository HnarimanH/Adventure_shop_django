from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProductSerializer, CreateProductSerializer
from rest_framework import status
from .models import Product

# Create your views here


class ProductView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class CreateProductView(APIView):
    def post(self, request):
        serializer = ProductSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteProductView(APIView):
    def delete(self, request):
        try:
            name = request.data.get("name")
            if not name:
                return Response({"error": "Product name is required"}, status=400)

            productToDelete = Product.objects.get(name=name)
            productToDelete.delete()

            return Response({"message": f"Deleted product '{name}'"}, status=200)

        except Product.DoesNotExist:
            return Response({"error": f"No product found with name '{name}'"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
        
        
        
        
class UpdateProductView(APIView):
    def post(self, request):
        try:
            product_id = request.data.get("id")
            if not product_id:
                return Response({"error": "Product id is required"}, status=400)
            
            productToUpdate = Product.objects.get(id=product_id)
            productToUpdate.name = request.data.get("name")
            productToUpdate.description = request.data.get("description")
            productToUpdate.price = request.data.get("price")
            productToUpdate.category = request.data.get("category")
            productToUpdate.image_url = request.data.get("image_url")  
            productToUpdate.save()

            return Response({"message": f"Updated product with id = '{product_id}'"}, status=200)
        
        except Product.DoesNotExist:
            return Response({"error": f"No product found with id '{product_id}'"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)