from django.shortcuts import render, HttpResponseRedirect
from .forms import *

# Create your views here.

def homepage(request):
    recipe_categories = MainCategory.objects.all()
    recipes_active = Recipe.objects.all().filter(active ='a').order_by('category')
    recipes_inactive = Recipe.objects.all().filter(active ='i')
    title='Συνταγές'
    context ={
        'title':title,
        'categories':recipe_categories,
        'recipes':recipes_active,
        'recipes_ina':recipes_inactive,
    }

    return render(request,'recipes_manager/homepage.html', context)


def new_recipe(request):
    recipe_categories = MainCategory.objects.all()
    recipes_active = Recipe.objects.all().filter(active ='a')
    recipes_inactive = Recipe.objects.all().filter(active ='i')
    title='Νέα Συνταγή'
    if request.POST:
        form = NewRecipeForm(request.POST)
        if form.is_valid():
            form.save()
            id= Recipe.objects.all().last().id
            return HttpResponseRedirect('/συνταγές/προσθήκη/%s' %(id))
    else:
        form = NewRecipeForm()

    context={
        'title':title,
        'categories':recipe_categories,
        'recipes':recipes_active,
        'recipes_ina':recipes_inactive,
        'form':form,

    }
    context.update(csrf(request))
    return render(request,'recipes_manager/new_recipe.html',context)



def recipes_per_category(request, dk):
    category = MainCategory.objects.get(id=dk)
    title = category.title
    recipes = Recipe.objects.all().filter(category__id= category.id)
    recipe_categories = MainCategory.objects.all()

    context = {
        'recipes':recipes,
        'title':title,
        'category':category,
        'categories':recipe_categories,
    }
    return render(request, 'recipes_manager/recipe_categories.html', context)


def activate_deactivate_recipe(request,dk,pk):
    cat = MainCategory.objects.get(id =dk)
    recipe = Recipe.objects.get(id=pk)
    if recipe.active == 'a':
        recipe.active ='i'
        recipe.save()

    elif recipe.active == 'i':
        recipe.active = 'a'
        recipe.save()
    return HttpResponseRedirect('/συνταγές/κατηγορία/%s/'%(cat.id))



def add_product_to_recipe(request,dk):
    recipe_categories = MainCategory.objects.all()
    recipe = Recipe.objects.get(id=dk)
    recipe_items =RecipeItem.objects.all().filter(recipe__title=recipe.title)
    if request.POST:
        form = NewRecipeItem(request.POST,initial={'recipe':recipe})
        if form.is_valid():
            form.save()
            form.price_cost()
            return HttpResponseRedirect('/διαχείρηση_εστιατορίου/συνταγές/προσθήκη/')
    else:
        form = NewRecipeItem(initial={'recipe':recipe})

    context={
        'recipe':recipe,
        'form_i':form,
        'recipe_items': recipe_items,
        'categories':recipe_categories,

    }
    
    return render(request,'recipes_manager/add_product_to_recipe.html',context)


def edit_recipe_id(request,dk):
    recipes = Recipe.objects.all()
    recipe = Recipe.objects.get(id=dk)
    recipe_items = recipe.recipeitem_set.all()
    recipe_categories = MainCategory.objects.all()


    if request.POST:
        form = NewRecipeForm(request.POST,instance=recipe)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/συνταγές/προσθήκη/%s' %(dk))
    else:
        form = NewRecipeForm(instance=recipe)

    context ={
        'form':form,
        'recipe':recipe,
        'recipes':recipes,
        'items':recipe_items,
        'categories':recipe_categories,
         'recipe_items': recipe_items,
    }
    
    return render(request, 'recipes_manager/edit_recipe_id_Νew.html',context)






def choose_product_to_recipe(request,dk):
    recipe_categories = MainCategory.objects.all()
    recipe = Recipe.objects.get(id=dk)
    recipe_items =RecipeItem.objects.all().filter(recipe__title=recipe.title)
    if request.POST:
        form = NewRecipeItem(request.POST,initial={'recipe':recipe})
        if form.is_valid():
            form.save()
            form.price_cost()
            return HttpResponseRedirect('/συνταγές/προσθήκη/%s' %(dk))
    else:
        form = NewRecipeItem(initial={'recipe':recipe})

    context={
        'recipe':recipe,
        'form':form,
        'recipe_items': recipe_items,
        'categories':recipe_categories,


    }
    
    return render(request,'recipes_manager/choose_product_to_recipe.html',context)



def edit_recipe_item_id(request,dk,pk):
    recipe_categories = MainCategory.objects.all()
    recipes = Recipe.objects.all()
    recipe = Recipe.objects.get(id=dk)
    recipe_items = recipe.recipeitem_set.all()
    recipe_item = RecipeItem.objects.get(id=pk)
    if request.POST:
        form = NewRecipeItem(request.POST,instance=recipe_item)
        if form.is_valid():
            form.save(commit=False)
            form.edit_recipe_item(dk=pk)
            return  HttpResponseRedirect('/συνταγές/προσθήκη/%s' %(dk))
    else:
        form= NewRecipeItem(instance=recipe_item)

    context={
        'recipe_item':recipe_item,
        'form':form,
        'recipe':recipe,
        'recipes':recipes,
        'recipe_items':recipe_items,
        'categories':recipe_categories,
    }
    
    return render(request,'recipes_manager/edit_recipe_item_id.html',context)

def delete_recipe(request,dk):
    recipe = Recipe.objects.get(id=dk)
    recipe_items = recipe.recipeitem_set.all()
    for ele in recipe_items:
        ele.delete()
    recipe.delete()
    return HttpResponseRedirect('/διαχείρηση_εστιατορίου/συνταγές/αλλαγές/')




def recipe_categories(request):
    recipe_categories = MainCategory.objects.all()
    if request.POST:
        form = CategoryEdit(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/συνταγές/κατηγορίες/')
    else:
        form = CategoryEdit()

    context ={
        'form':form,
        'categories':recipe_categories,
    }
    
    return render(request, 'recipes_manager/categories_section.html', context)


def edit_recipe_categories(request,dk):
    category = MainCategory.objects.get(id=dk)
    recipe_categories = MainCategory.objects.all()
    if request.POST:
        form = CategoryEdit(request.POST,instance=category)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/συνταγές/κατηγορίες/')
    else:
        form = CategoryEdit(instance=category)

    context ={
        'form':form,
        'categories':recipe_categories,
    }
    
    return render(request, 'recipes_manager/categories_section.html', context)




#---------------------------------------------------------------------------------------------



def edit_delete_recipe_item(request,dk):
    recipe_item = RecipeItem.objects.get(id=dk)
    recipe_item.delete_recipe_item(dk=dk)
    return HttpResponseRedirect('/διαχείρηση_εστιατορίου/συνταγές/αλλαγές/')







def delete_recipe_item(request,dk):
    recipe_item = RecipeItem.objects.get(id=dk)
    recipe_item.delete_recipe_item(dk=dk)
    return HttpResponseRedirect('/διαχείρηση_εστιατορίου/συνταγές/προσθήκη/')


def cost_estimation(request):
    recipes = Recipe.objects.all()
    context = {
        'recipes':recipes
    }
    return render(request,'recipes_manager/cost_estimation.html',context)






def menu_homepage(request):
    recipes =Recipe.objects.all().filter(active='a').order_by('category')
    context = {
        'recipes':recipes
    }
    return render(request,'recipes_manager/menu_homepage.html',context)



def edit_recipe(request):
    recipes = Recipe.objects.all()
    context ={
        'recipes':recipes,
        }
    return render(request,'recipes_manager/edit_recipe.html',context)





def show_recipe_items(request,dk,pk):
    category = MainCategory.objects.get(id=dk)
    recipe_categories = MainCategory.objects.all()
    recipe = Recipe.objects.get(id= pk)
    title = recipe.title
    recipe_items = recipe.recipeitem_set.all()
    recipes = Recipe.objects.all().filter(category__id= category.id)

    context = {
        'title':title,
        'category':category,
        'categories':recipe_categories,
        'recipe_items':recipe_items,
        'recipe':recipe,
        'recipes':recipes,
    }
    return render(request, 'recipes_manager/recipe_category_id.html', context)
