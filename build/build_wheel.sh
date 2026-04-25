directory_list=(
    "locale"
)
target_dir="paramdict"
target_files=(
    "LICENSE"
    "README.md"
)

if [ ! -d "$target_dir" ]; then
    mkdir "$target_dir"
fi

pyfilenum=$(ls "$target_dir" | grep "\.py$" | wc -l)
if [ "$pyfilenum" -gt 0 ]; then
    rm "$target_dir"/*.py
fi
for dir in "${directory_list[@]}"; do
    if [ -d "$target_dir/$dir" ]; then
        rm -r "$target_dir/$dir"
    fi
done
for file in "${target_files[@]}"; do
    if [ -f "$file" ]; then
        rm "$file"
    fi
done

if [ -d "build" ]; then
    rm -r build
fi

cp ../*.py "$target_dir"/
for dir in "${directory_list[@]}"; do
    cp -r ../"$dir" "$target_dir"/
done
for file in "${target_files[@]}"; do
    cp ../$file ./
done

python -m build --wheel
