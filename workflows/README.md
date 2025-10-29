# ComfyUI Workflow Templates

This directory contains modular JSON templates for building ComfyUI workflows dynamically.

## Structure

### Core Workflow
- **`basic_workflow.json`** - Base workflow with KSampler, checkpoint loader, prompt encoding, VAE decode, and save image

### Optional Nodes
- **`lora_loader.json`** - LoRA model loader (applied only for INTIMATE images)
- **`upscale_node.json`** - 2x image upscaling using ImageScaleBy
- **`facedetailer_node.json`** - Face refinement with FaceDetailer + UltralyticsDetectorProvider

## Template Syntax

Templates use `{{placeholder}}` syntax for dynamic values:

```json
{
  "inputs": {
    "seed": "{{seed}}",
    "steps": "{{steps}}",
    "checkpoint": "{{checkpoint}}"
  }
}
```

## Workflow Builder

The `WorkflowBuilder` class in `app.py` handles:
1. Loading JSON templates
2. Replacing placeholders with actual values
3. Combining modules based on configuration
4. Building complete workflows

## Usage Example

```python
workflow = WorkflowBuilder.build_workflow(
    image_type="INTIMATE",
    use_lora=True,           # Add LoRA for INTIMATE
    use_upscale=True,        # Add 2x upscaling
    use_facedetailer=True,   # Add face refinement
    steps=15,
    checkpoint="model.safetensors",
    width=768,
    height=768,
    positive_prompt="...",
    negative_prompt="..."
)
```

## Workflow Flow

### Basic (No Options)
```
EmptyLatent → KSampler → VAEDecode → SaveImage
```

### With Upscale
```
EmptyLatent → KSampler → VAEDecode → ImageScaleBy (2x) → SaveImage
```

### With FaceDetailer
```
EmptyLatent → KSampler → VAEDecode → FaceDetailer → SaveImage
```

### With LoRA
```
CheckpointLoader → LoraLoader → KSampler → VAEDecode → SaveImage
```

### Full Pipeline (All Options)
```
CheckpointLoader → LoraLoader → KSampler → VAEDecode → ImageScaleBy → FaceDetailer → SaveImage
```

## Node IDs

| Node ID | Purpose |
|---------|---------|
| 3 | KSampler (main generation) |
| 4 | CheckpointLoaderSimple |
| 5 | EmptyLatentImage |
| 6 | CLIPTextEncode (positive) |
| 7 | CLIPTextEncode (negative) |
| 8 | VAEDecode |
| 9 | SaveImage |
| 10 | FaceDetailer |
| 11 | LoraLoader |
| 12 | UltralyticsDetectorProvider |
| 15 | ImageScaleBy (upscale) |

## Placeholders

### Basic Workflow
- `{{seed}}` - Random seed for generation
- `{{steps}}` - Number of sampling steps
- `{{checkpoint}}` - Checkpoint model filename
- `{{width}}` - Image width
- `{{height}}` - Image height
- `{{positive_prompt}}` - Positive prompt text
- `{{negative_prompt}}` - Negative prompt text
- `{{model_source}}` - Model node reference [node_id, output_index]
- `{{clip_source}}` - CLIP node reference [node_id, output_index]
- `{{image_source}}` - Image node reference [node_id, output_index]

### LoRA Loader
- `{{lora_name}}` - LoRA model filename
- `{{lora_strength}}` - LoRA strength (0.0-1.0)

### FaceDetailer
- `{{facedetailer_steps}}` - FaceDetailer sampling steps
- `{{facedetailer_denoise}}` - FaceDetailer denoise strength

## Smart Features

### 1. Smart LoRA Usage
- **CASUAL/FLIRTY**: No LoRA (natural look)
- **INTIMATE**: Anatomical detail LoRA applied

### 2. Conditional Upscaling
- **Enabled**: 768x768 → 1536x1536
- **Disabled**: Direct 768x768 output

### 3. Optional FaceDetailer
- **Enabled**: Face refinement after generation
- **Disabled**: Skip for faster generation

## Adding New Nodes

1. Create new JSON file in `workflows/` directory
2. Use `{{placeholder}}` syntax for dynamic values
3. Load in `WorkflowBuilder.build_workflow()`
4. Add to workflow with `workflow.update(new_node)`

Example:
```json
// workflows/my_custom_node.json
{
  "99": {
    "inputs": {
      "parameter": "{{my_param}}",
      "image": ["8", 0]
    },
    "class_type": "MyCustomNode"
  }
}
```

```python
# In WorkflowBuilder.build_workflow()
if use_custom_node:
    custom_node = WorkflowBuilder.load_workflow_template('my_custom_node')
    custom_replacements = {'my_param': params.get('my_param', 'default')}
    custom_node = WorkflowBuilder.replace_placeholders(custom_node, custom_replacements)
    workflow.update(custom_node)
```

## Benefits

✅ **Modular** - Easy to add/remove nodes  
✅ **Maintainable** - JSON templates are easy to edit  
✅ **Flexible** - Dynamic workflow building  
✅ **Reusable** - Templates can be shared  
✅ **Version Control** - JSON diffs are readable  
✅ **Testable** - Templates can be validated  

## Configuration

Workflows are configured via environment variables in `.env`:

```env
# LoRA
ENABLE_LORA=true

# FaceDetailer
ENABLE_FACE_DETAILER=true
FACEDETAILER_STEPS=15
FACEDETAILER_DENOISE=0.35

# Upscaling
ENABLE_UPSCALE=true

# Generation
IMAGE_GENERATION_STEPS=15
```

## Troubleshooting

### Template not found
```
Warning: Workflow template xxx not found, using fallback
```
**Solution:** Check that JSON file exists in `workflows/` directory

### Placeholder not replaced
```
{{placeholder}} appears in final workflow
```
**Solution:** Add placeholder to `replacements` dict in `build_workflow()`

### Node connection error
```
Node X output not found
```
**Solution:** Check node ID references match between templates

## Future Enhancements

- [ ] ControlNet template
- [ ] img2img template
- [ ] Multiple LoRA support
- [ ] Custom sampler templates
- [ ] Workflow validation
- [ ] Template versioning
