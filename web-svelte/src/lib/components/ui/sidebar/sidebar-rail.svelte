<script lang="ts">
	import { cn, type WithElementRef } from "$lib/utils.js";
	import type { HTMLAttributes } from "svelte/elements";
	import { SIDEBAR_MAX_WIDTH, SIDEBAR_MIN_WIDTH } from "./constants.js";
	import { useSidebar } from "./context.svelte.js";

	let {
		ref = $bindable(null),
		class: className,
		children,
		...restProps
	}: WithElementRef<HTMLAttributes<HTMLButtonElement>, HTMLButtonElement> = $props();

	const sidebar = useSidebar();
	
	let isResizing = $state(false);
	let startX = $state(0);
	let startWidth = $state(0);
	let clickTime = $state(0);
	let clickX = $state(0);

	function parseRem(value: string): number {
		return parseFloat(value.replace("rem", "")) * 16;
	}

	function formatRem(pixels: number): string {
		return `${pixels / 16}rem`;
	}

	function handleMouseDown(e: MouseEvent) {
		// Check if this is a click (not a drag)
		clickTime = Date.now();
		clickX = e.clientX;
		
		// Start resizing
		isResizing = true;
		startX = e.clientX;
		startWidth = parseRem(sidebar.width);
		
		document.addEventListener("mousemove", handleMouseMove);
		document.addEventListener("mouseup", handleMouseUp);
		e.preventDefault();
	}

	function handleMouseMove(e: MouseEvent) {
		if (!isResizing) return;
		
		const deltaX = e.clientX - startX;
		// For left sidebars, dragging right increases width, dragging left decreases it
		const newWidthPx = startWidth + deltaX;
		
		const minWidth = parseRem(SIDEBAR_MIN_WIDTH);
		const maxWidth = parseRem(SIDEBAR_MAX_WIDTH);
		const clampedWidth = Math.max(minWidth, Math.min(maxWidth, newWidthPx));
		
		sidebar.setWidth(formatRem(clampedWidth));
	}

	function handleMouseUp(e: MouseEvent) {
		if (!isResizing) return;
		
		// Check if this was a click (not a drag)
		const timeDiff = Date.now() - clickTime;
		const xDiff = Math.abs(e.clientX - clickX);
		
		if (timeDiff < 200 && xDiff < 5) {
			// It was a click, toggle the sidebar
			sidebar.toggle();
		}
		
		isResizing = false;
		document.removeEventListener("mousemove", handleMouseMove);
		document.removeEventListener("mouseup", handleMouseUp);
	}
</script>

<button
	bind:this={ref}
	data-sidebar="rail"
	data-slot="sidebar-rail"
	aria-label="Toggle Sidebar"
	tabIndex={-1}
	onmousedown={handleMouseDown}
	title="Drag to resize, click to toggle"
	class={cn(
		"hover:after:bg-sidebar-border absolute inset-y-0 z-20 hidden w-4 -translate-x-1/2 transition-all ease-linear after:absolute after:inset-y-0 after:start-[calc(1/2*100%-1px)] after:w-[2px] group-data-[side=left]:-end-4 group-data-[side=right]:start-0 sm:flex",
		"in-data-[side=left]:cursor-w-resize in-data-[side=right]:cursor-e-resize",
		"[[data-side=left][data-state=collapsed]_&]:cursor-e-resize [[data-side=right][data-state=collapsed]_&]:cursor-w-resize",
		"hover:group-data-[collapsible=offcanvas]:bg-sidebar group-data-[collapsible=offcanvas]:translate-x-0 group-data-[collapsible=offcanvas]:after:start-full",
		"[[data-side=left][data-collapsible=offcanvas]_&]:-end-2",
		"[[data-side=right][data-collapsible=offcanvas]_&]:-start-2",
		isResizing ? "cursor-w-resize" : "",
		className
	)}
	{...restProps}
>
	{@render children?.()}
</button>
