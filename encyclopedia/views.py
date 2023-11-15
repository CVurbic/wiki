from django.shortcuts import render,redirect
from django.http import Http404
from . import util
import random
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "error_message": "Page not found"
        })
    

    return render(request, "encyclopedia/entry_page.html", {
        "title": title,
        "content": markdown2.markdown(content),
    })


def search_result(request):
    query = request.GET.get('q')
    entries = util.list_entries()

    exact_match = util.get_entry(query)
    print(f"Query: {query}, Exact Match: {exact_match}")

    if exact_match:
        return redirect('entry_page', title=query)
    else:
        search_result = [entry for entry in entries if query.lower() in entry.lower()]
        print(f"Search Result: {search_result}")
        return render(request, "encyclopedia/search_result.html", {
            "query": query,
            "results": search_result
        })
  
def new_page(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        existing_entry = util.get_entry(title)
        if existing_entry:
            return render(request, "encyclopedia/error.html", {
                "error_message": "An entry You tried to create already exists. Edit that one or create another."
            })

        util.save_entry(title, content)
        return redirect('entry_page', title=title)

    return render(request, "encyclopedia/new_page.html")

def edit_page(request, title):
    existing_content = util.get_entry(title)

    if request.method == "POST":
        content = request.POST.get("content")
        util.save_entry(title, content)
        return redirect('entry_page', title=title)

    return render(request, "encyclopedia/edit_page.html", {"title": title, "content": existing_content})


def random_page(request):
    entries = util.list_entries()
    if entries:
        random_title = random.choice(entries)
        return redirect('entry_page', title=random_title)
    else:
        return render(request, "encyclopedia/error.html", {
            "error_message": "No entries exist."
        })