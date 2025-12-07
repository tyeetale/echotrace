<script lang="ts">
  import { Action, Actions } from "$lib/components/ai-elements/action/index.js";
  import {
    Message,
    MessageAvatar,
    MessageContent,
  } from "$lib/components/ai-elements/message/index.js";
  import {
    PromptInput,
    PromptInputActionAddAttachments,
    PromptInputActionMenu,
    PromptInputActionMenuContent,
    PromptInputActionMenuTrigger,
    PromptInputAttachment,
    PromptInputAttachments,
    PromptInputBody,
    PromptInputButton,
    PromptInputModelSelect,
    PromptInputModelSelectContent,
    PromptInputModelSelectItem,
    PromptInputModelSelectTrigger,
    PromptInputModelSelectValue,
    PromptInputSubmit,
    PromptInputTextarea,
    PromptInputToolbar,
    PromptInputTools,
  } from "$lib/components/ai-elements/prompt-input/index.js";
  import AppSidebar from "$lib/components/app-sidebar.svelte";
  import * as Breadcrumb from "$lib/components/ui/breadcrumb/index.js";
  import { Separator } from "$lib/components/ui/separator/index.js";
  import * as Sidebar from "$lib/components/ui/sidebar/index.js";

  type MessageData = {
    key: string;
    from: "user" | "assistant";
    content: string;
    avatar: string;
    name: string;
  };

  let messages: MessageData[] = $state([
    {
      key: crypto.randomUUID(),
      from: "user",
      content: "Hello, how are you?",
      avatar: "https://github.com/haydenbleasel.png",
      name: "Hayden Bleasel",
    },
    {
      key: crypto.randomUUID(),
      from: "assistant",
      content:
        "Hello! I'm doing well, thank you for asking. How can I help you today?",
      avatar: "https://github.com/copilot.png",
      name: "Assistant",
    },
    {
      key: crypto.randomUUID(),
      from: "user",
      content: "Can you help me understand Svelte 5 runes?",
      avatar: "https://github.com/haydenbleasel.png",
      name: "Hayden Bleasel",
    },
    {
      key: crypto.randomUUID(),
      from: "assistant",
      content:
        "Absolutely! Svelte 5 introduces runes like $state, $derived, and $props which provide a more powerful and flexible reactivity system. Would you like me to explain any specific rune?",
      avatar: "https://github.com/copilot.png",
      name: "Assistant",
    },
  ]);
</script>

<Sidebar.Provider>
  <AppSidebar />
  <Sidebar.Inset>
    <header class="flex h-16 shrink-0 items-center gap-2 border-b px-4">
      <Sidebar.Trigger class="-ms-1" />
      <Separator
        orientation="vertical"
        class="me-2 data-[orientation=vertical]:h-4"
      />
      <Breadcrumb.Root>
        <Breadcrumb.List>
          <Breadcrumb.Item class="hidden md:block">
            <Breadcrumb.Link href="##">lib</Breadcrumb.Link>
          </Breadcrumb.Item>
          <Breadcrumb.Separator class="hidden md:block" />
          <Breadcrumb.Item class="hidden md:block">
            <Breadcrumb.Link href="##">components</Breadcrumb.Link>
          </Breadcrumb.Item>
          <Breadcrumb.Separator class="hidden md:block" />
          <Breadcrumb.Item>
            <Breadcrumb.Page>button.svelte</Breadcrumb.Page>
          </Breadcrumb.Item>
        </Breadcrumb.List>
      </Breadcrumb.Root>
    </header>
    <!-- don't use full width, use max-w-7xl -->
    <main class="flex-1 overflow-y-auto max-w-2xl mx-auto p-4">
      <!-- create a chat interface here -->
      <div class="space-y-4">
        {#each messages as { content, from, avatar, name }}
          <Message {from}>
            <MessageContent>{content}</MessageContent>
            <MessageAvatar {name} src={avatar} />
          </Message>
        {/each}

        <Actions>
          <Action></Action>
        </Actions>

        <PromptInput globalDrop multiple onSubmit={handleSubmit}>
          <PromptInputBody>
            <PromptInputAttachments>
              {#snippet children(attachment)}
                <PromptInputAttachment data={attachment} />
              {/snippet}
            </PromptInputAttachments>
            <PromptInputTextarea
              bind:value={text}
              onchange={(e) => (text = (e.target as HTMLTextAreaElement).value)}
            />
          </PromptInputBody>
          <PromptInputToolbar>
            <PromptInputTools>
              <PromptInputActionMenu>
                <PromptInputActionMenuTrigger />
                <PromptInputActionMenuContent>
                  <PromptInputActionAddAttachments />
                </PromptInputActionMenuContent>
              </PromptInputActionMenu>
              <PromptInputButton>
                <MicIcon size={16} />
              </PromptInputButton>
              <PromptInputButton size="default">
                <GlobeIcon size={16} />
                <span>Search</span>
              </PromptInputButton>
              <PromptInputModelSelect
                bind:value={model}
                onValueChange={(value) => {
                  if (value) {
                    model = value;
                    const selectedModel = models.find((m) => m.id === model);
                    model_name = selectedModel ? selectedModel.name : "";
                  }
                }}
              >
                <PromptInputModelSelectTrigger>
                  <PromptInputModelSelectValue
                    value={model_name}
                    placeholder="Select Model"
                  />
                </PromptInputModelSelectTrigger>
                <PromptInputModelSelectContent>
                  {#each models as modelOption (modelOption.id)}
                    <PromptInputModelSelectItem value={modelOption.id}>
                      {modelOption.name}
                    </PromptInputModelSelectItem>
                  {/each}
                </PromptInputModelSelectContent>
              </PromptInputModelSelect>
            </PromptInputTools>
            <PromptInputSubmit {status} />
          </PromptInputToolbar>
        </PromptInput>
      </div>
    </main>
  </Sidebar.Inset>
</Sidebar.Provider>
